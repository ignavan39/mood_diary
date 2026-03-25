import asyncio
import logging
from typing import TYPE_CHECKING, Callable

from presentation.common.base_bot import BaseBot
from presentation.vk.handlers.router import VkRouter, create_vk_router
from presentation.vk.polling import VkLongPolling
from presentation.vk.sdk.types import VkMessage

if TYPE_CHECKING:
    from infrastructure import AppContainer

logger = logging.getLogger(__name__)


class VkBot(BaseBot):
    def __init__(
        self,
        container: "AppContainer",
        token: str,
        group_id: int,
    ) -> None:
        super().__init__(container)
        self._group_id = group_id
        self._token = token
        self._container = container

        self._polling: VkLongPolling | None = None
        self._router: VkRouter | None = None
        self._main_loop: asyncio.AbstractEventLoop | None = None

    def _create_message_handler(self, router: VkRouter) -> Callable[[VkMessage], bool]:
        def handle_message(message) -> bool:
            if self._main_loop and not self._main_loop.is_closed():
                try:
                    asyncio.run_coroutine_threadsafe(
                        router.route(message),
                        self._main_loop,
                    )
                    return True
                except Exception as e:
                    logger.error("Failed to schedule message routing: %s", e)
                    return False
            else:
                logger.warning("Main loop not available, skipping message")
                return False

        return handle_message

    async def start(self) -> None:
        logger.info("Starting VK Bot...")

        self._main_loop = asyncio.get_running_loop()

        import vk_api

        vk = vk_api.VkApi(token=self._token)
        self._router = create_vk_router(vk, self._container, self._group_id)

        self._polling = VkLongPolling(
            token=self._token,
            group_id=self._group_id,
            on_message=self._create_message_handler(self._router),
        )

        def on_polling_error(error: Exception) -> None:
            logger.error("Polling error: %s", error)

        self._polling.start(
            main_loop=self._main_loop,
            on_error=on_polling_error,
        )

        await asyncio.sleep(0.5)

        if self._polling and self._polling.is_running:
            logger.info("VK Bot started (polling active)")
        else:
            logger.error("Failed to start VK Bot polling")

    async def stop(self) -> None:
        logger.info("Stopping VK Bot...")

        if self._polling:
            self._polling.stop(timeout=30)

        logger.info("VK Bot stopped")

    @staticmethod
    def get_platform_name() -> str:
        return "vk"


def create_vk_bot(container: "AppContainer") -> "VkBot | None":
    from infrastructure.configs.config import settings

    if settings.vk_bot is None or not settings.vk_bot.enabled:
        logger.info("VK bot disabled")
        return None

    logger.info("VK bot enabled for group_id=%d", settings.vk_bot.group_id)

    return VkBot(
        container=container,
        token=settings.vk_bot.token,
        group_id=settings.vk_bot.group_id,
    )


__all__ = ["VkBot", "create_vk_bot"]
