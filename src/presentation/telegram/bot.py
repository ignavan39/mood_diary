import logging
from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from infrastructure.configs import settings
from presentation.common.base_bot import BaseBot
from presentation.telegram.commands import commands
from presentation.telegram.endpoints.help import help_router
from presentation.telegram.endpoints.mood import mood_router
from presentation.telegram.endpoints.user import user_router
from presentation.telegram.middlewares import ErrorHandlerMiddleware, MetricsMiddleware

if TYPE_CHECKING:
    from infrastructure import AppContainer

logger = logging.getLogger(__name__)


class TelegramBot(BaseBot):
    def __init__(self, container: "AppContainer", token: str) -> None:
        super().__init__(container)
        session = AiohttpSession(timeout=120)

        self._bot = Bot(
            token=token,
            default=DefaultBotProperties(parse_mode="HTML"),
            session=session,
        )
        self._dp = Dispatcher()

        self._dp.message.middleware(MetricsMiddleware())
        self._dp.callback_query.middleware(MetricsMiddleware())

        self._dp.message.middleware(ErrorHandlerMiddleware())
        self._dp.callback_query.middleware(ErrorHandlerMiddleware())

        self._dp.include_routers(user_router, mood_router, help_router)
        self._dp.startup.register(self._on_startup)

    async def _on_startup(self) -> None:
        await self._bot.set_my_commands(commands)
        logger.info("Bot commands registered")

    async def start(self) -> None:
        logger.info("🚀 Starting Telegram Bot (polling)...")
        await self._dp.start_polling(self._bot)

    async def stop(self) -> None:
        logger.info("Stopping Telegram Bot...")
        await self._bot.session.close()
        await self._bot.close()
        logger.info("Telegram Bot stopped")

    @staticmethod
    def get_platform_name() -> str:
        return "telegram"


def create_telegram_bot(container: "AppContainer") -> "TelegramBot | None":
    if not settings.tg_bot.enabled or settings.tg_bot.token is None:
        logger.info(
            "TG__BOT_TOKEN not set Telegram bot disabled (TG_BOT_ENABLED=false)"
        )
        return None

    return TelegramBot(container, token=settings.tg_bot.token)
