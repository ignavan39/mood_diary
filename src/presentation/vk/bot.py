import logging

from vkbottle import API
from vkbottle.bot import Bot as VKBot
from vkbottle.polling import BotPolling

from presentation.common.base_bot import BaseBot
from presentation.vk.endpoints.help.router import register_help_handlers

from infrastructure.ioc.container.application import AppContainer
from presentation.vk.endpoints.user import register_user_handlers

logger = logging.getLogger(__name__)


class VkBot(BaseBot):
    def __init__(self, container: "AppContainer", token: str, group_id: int) -> None:
        super().__init__(container)
        self._group_id = group_id
        self._vk = VKBot(token=token)
        self._api = API(token=token)
        self._register_handlers()

    def _register_handlers(self) -> None:
        register_help_handlers(self._vk)
        register_user_handlers(self._vk, self._api, self._container)

    async def start(self) -> None:
        logger.info("🚀 Starting VK Bot (long polling)...")
        polling = BotPolling(
            api=self._vk.api,
            error_handler=self._vk.error_handler,
            group_id=self._group_id,
        )
        polling.listen()

    async def stop(self) -> None:
        logger.info("Stopping VK Bot...")

    @staticmethod
    def get_platform_name() -> str:
        return "vk"


def create_vk_bot(container: "AppContainer") -> "VkBot | None":
    from infrastructure.configs.config import settings

    if settings.vk_bot is None or not settings.vk_bot.enabled:
        logger.info("VK bot disabled (VK_BOT_TOKEN not set or VK_BOT_ENABLED=false)")
        return None

    logger.info("VK bot enabled for group_id=%d", settings.vk_bot.group_id)
    return VkBot(
        container=container,
        token=settings.vk_bot.token,
        group_id=settings.vk_bot.group_id,
    )
