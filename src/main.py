import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher

from infrastructure.configs import settings
from infrastructure.database import get_session_manager
from infrastructure.telegram.handlers.user import router as user_router

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


async def on_startup(bot: Bot):
    me = await bot.get_me()
    logger.info(f"🤖 Bot started: @{me.username}")


async def on_shutdown(bot: Bot):
    logger.info("🛑 Bot stopped")
    await bot.session.close()
    await get_session_manager().close()


async def async_main() -> None:
    bot = Bot(settings.tg_bot.token)

    dp = Dispatcher()

    get_session_manager()

    logger.info("Starting mood_diary bot...")
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(user_router)

    await dp.start_polling(bot)
    logger.info("📡 Polling stopped")


if __name__ == "__main__":
    asyncio.run(async_main())
