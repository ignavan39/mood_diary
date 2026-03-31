import logging
from abc import ABC, abstractmethod
from typing import ClassVar

from infrastructure import AppContainer
from presentation.vk.sdk.types import VkMessage
from presentation.vk.types import Context
from presentation.vk.sdk.api import VkSdk

logger = logging.getLogger(__name__)
PLATFORM = "vk"


class VkHandler(ABC):
    COMMANDS: ClassVar[tuple[str, ...]] = ()

    def __init__(
        self,
        vk_api: "VkSdk",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        self._api = vk_api
        self._group_id = group_id

    @abstractmethod
    async def handle(self, message: VkMessage, ctx: Context) -> bool: ...

    async def handle_with_metrics(self, message: VkMessage, ctx: Context) -> bool:
        import time
        from infrastructure.metrics import bot_messages_total, bot_request_duration

        start = time.perf_counter()
        status = "success"
        matched = False

        try:
            matched = await self.handle(message, ctx)
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
