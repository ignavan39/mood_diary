import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from infrastructure import AppContainer
from infrastructure.configs import settings
from presintation.common.base_bot import BaseBot
from presintation.telegram.commands import commands
from presintation.telegram.endpoints.help import help_router
from presintation.telegram.endpoints.mood import mood_router
from presintation.telegram.endpoints.user import user_router


logger = logging.getLogger(__name__)


class TelegramBot(BaseBot):
    def __init__(self, container: "AppContainer") -> None:
        super().__init__(container)

    async def create(self, container: "AppContainer"):
        self._bot = Bot(
            token=settings.tg_bot.token, default=DefaultBotProperties(parse_mode="HTML")
        )
        self._dp = Dispatcher()

        self._dp.include_routers(user_router, mood_router, help_router)

        logger.info("✅ Telegram Bot initialized")

    async def start(self) -> None:
        logger.info("🚀 Starting Telegram Bot (polling)...")

        await self._bot.set_my_commands(commands)

        await self._dp.start_polling(self._bot)

    async def stop(self) -> None:
        logger.info("🛑 Stopping Telegram Bot...")
        await self._bot.session.close()
        await self._bot.close()
        logger.info("✅ Telegram Bot stopped")

    @staticmethod
    def get_platform_name() -> str:
        return "Telegram"


def create_telegram_bot(container: "AppContainer") -> TelegramBot:
    return TelegramBot(container)
