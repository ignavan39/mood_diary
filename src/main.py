import asyncio
import logging
import sys
import threading
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from infrastructure.configs import settings
from infrastructure.ioc.container.application import AppContainer
from infrastructure.metrics import start_metrics_server
from presintation.telegram.endpoints.mood import mood_router
from presintation.telegram.endpoints.user import user_router

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
        self._container = AppContainer()

    async def _on_startup(self):
        self._container.infrastructure.session_manager()
        me = await self._bot.get_me()
        logger.info(f"🤖 Bot started: @{me.username}")

    async def _on_shutdown(self):
        logger.info("🛑 Bot stopped")
        await self._container.infrastructure.session_manager().close()
        await self._container.infrastructure.redis_cache().close()
        await self._bot.session.close()

    async def start(self):
        redis_manager = self._container.infrastructure.redis_cache()
        redis = await redis_manager.get_connection()
        fsm_storage = RedisStorage(
            redis=redis,
            state_ttl=3600,
            data_ttl=7200,
        )

        dp = Dispatcher(storage=fsm_storage)

        logger.info("FSM storage initialized (Redis-backend)")

        logger.info("Starting mood_diary bot...")
        dp.startup.register(self._on_startup)
        dp.shutdown.register(self._on_shutdown)

        dp.include_router(user_router)
        dp.include_router(mood_router)

        threading.Thread(target=start_metrics_server, daemon=True).start()

        bot = self._bot
        await dp.start_polling(bot)
        logger.info("📡 Polling stopped")


if __name__ == "__main__":
    app = App()
    asyncio.run(app.start())
