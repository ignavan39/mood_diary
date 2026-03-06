import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher

from infrastructure.configs import settings
from infrastructure.ioc.container.application import AppContainer
from presintation.telegram.user import user_router

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)


logger = logging.getLogger(__name__)
logger.info("Logging system initialized")


logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)

logging.getLogger("aiogram").setLevel(logging.INFO)
logging.getLogger("aiogram.events").setLevel(logging.INFO)


class App:
    def __init__(self):
        self._bot = Bot(settings.tg_bot.token)
        self._dp = Dispatcher()
        self._container = AppContainer()

    async def _on_startup(self):
        self._container.infrastructure.container.session_manager()
        me = await self._bot.get_me()
        logger.info(f"🤖 Bot started: @{me.username}")

    async def _on_shutdown(self):
        logger.info("🛑 Bot stopped")
        await self._container.infrastructure.container.session_manager().close()
        await self._bot.session.close()

    async def start(self):
        logger.info("Starting mood_diary bot...")
        self._dp.startup.register(self._on_startup)
        self._dp.shutdown.register(self._on_shutdown)

        self._dp.include_router(user_router)

        bot = self._bot
        await self._dp.start_polling(bot)
        logger.info("📡 Polling stopped")


if __name__ == "__main__":
    app = App()
    asyncio.run(app.start())
