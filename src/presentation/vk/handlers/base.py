import asyncio
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, Optional, Any

from infrastructure import AppContainer
from presentation.vk.sdk.types import VkMessage

if TYPE_CHECKING:
    from vk_api import VkApi

logger = logging.getLogger(__name__)
PLATFORM = "vk"


class VkHandler(ABC):
    COMMANDS: ClassVar[tuple[str, ...]] = ()

    def __init__(
        self,
        vk_api: "VkApi",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        self._vk = vk_api
        self._group_id = group_id

    @abstractmethod
    async def handle(self, message: VkMessage) -> bool: ...

    async def handle_with_metrics(self, message: VkMessage) -> bool:
        import time
        from infrastructure.metrics import bot_messages_total, bot_request_duration

        start = time.perf_counter()
        status = "success"
        matched = False

        try:
            matched = await self.handle(message)
            return matched
        except Exception:
            status = "error"
            matched = True
            raise
        finally:
            if matched:
                duration = time.perf_counter() - start
                command = self._command_label()

                bot_messages_total.labels(
                    platform=PLATFORM,
                    command=command,
                    status=status,
                ).inc()
                bot_request_duration.labels(
                    platform=PLATFORM,
                    command=command,
                ).observe(duration)

    def _matches_command(self, text: str) -> bool:
        text_normalized = text.lower().strip()
        return any(cmd.lower().strip() == text_normalized for cmd in self.COMMANDS)

    def _command_label(self) -> str:
        return self.__class__.__name__.replace("Handler", "").lower()

    async def _send_message(
        self,
        user_id: int,
        text: str,
        keyboard: Optional[str] = None,
        attachment: Optional[str] = None,
    ) -> bool:
        params = {
            "user_id": user_id,
            "message": text,
            "random_id": 0,
        }
        if keyboard:
            params["keyboard"] = keyboard
        if attachment:
            params["attachment"] = attachment

        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: self._vk.method("messages.send", params),
            )
            logger.debug("Sent to VK %d: %s", user_id, text[:50])
            return True
        except Exception as e:
            logger.error("Failed to send message to %d: %s", user_id, e)
            return False

    async def _answer_callback_event(
        self,
        event_id: str,
        user_id: int,
        action: Optional[dict] = None,
    ) -> bool:
        params = {
            "event_id": event_id,
            "user_id": user_id,
            "action": action or {},
        }

        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: self._vk.method("messages.sendMessageEventAnswer", params),
            )
            logger.debug("Callback answered: %s", event_id)
            return True
        except Exception as e:
            logger.error("Failed to answer callback %s: %s", event_id, e)
            return False

    async def _call_vk_method(self, method: str, params: dict[str, Any]) -> Any:
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._vk.method(method, params),
            )
            logger.debug("VK API call: %s with %s", method, params)
            return result
        except Exception as e:
            logger.error("VK API method %s failed: %s", method, e)
            raise
