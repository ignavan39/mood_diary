import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

from presentation.vk.sdk.types import VkMessage


if TYPE_CHECKING:
    from vk_api import VkApi
    from infrastructure import AppContainer

logger = logging.getLogger(__name__)


class VkHandler(ABC):
    COMMANDS: ClassVar[tuple[str, ...]] = ()

    def __init__(
        self,
        vk_api: "VkApi",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        self._vk = vk_api
        self._container = container
        self._group_id = group_id

    @abstractmethod
    async def handle(self, message: VkMessage) -> bool: ...

    def _matches_command(self, text: str) -> bool:
        text_lower = text.lower().strip()
        return any(cmd.lower() in text_lower for cmd in self.COMMANDS)

    async def _send_message(
        self,
        user_id: int,
        text: str,
        keyboard: str | None = None,
    ) -> None:
        import asyncio

        params = {
            "user_id": user_id,
            "message": text,
            "random_id": 0,
        }

        if keyboard:
            params["keyboard"] = keyboard

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: self._vk.method("messages.send", params),
        )

        logger.debug("Sent to VK %d: %s", user_id, text[:50])


__all__ = ["VkHandler"]
