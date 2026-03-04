import asyncio
from functools import partial
import logging
import sys
from aiogram import Bot, Dispatcher

from infrastructure.configs import settings
from infrastructure.database import DatabaseSessionManager
from infrastructure.telegram import DatabaseSessionMiddleware
from infrastructure.telegram.handlers.user import create_user_handler

logger = logging.getLogger(__name__)
logger.info("🔧 Logging system initialized")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)


async def on_startup(bot: Bot):
    me = await bot.get_me()
    logger.info(f"🤖 Bot started: @{me.username}")


async def on_shutdown(bot: Bot, db_manager: DatabaseSessionManager):
    logger.info("🛑 Bot stopped")
    await bot.session.close()
    await db_manager.close()


async def async_main() -> None:
    bot = Bot(settings.tg_bot.token)

    dp = Dispatcher()
    session_manager = DatabaseSessionManager(settings.db.get_url())

    logger.info("Starting mood_diary bot...")
    dp.startup.register(on_startup)
    dp.shutdown.register(partial(on_shutdown, bot, session_manager))

    dp.message.middleware(DatabaseSessionMiddleware(session_manager))
    dp.callback_query.middleware(DatabaseSessionMiddleware(session_manager))

    create_user_handler(router=dp)

    await dp.start_polling(bot)
    logger.info("📡 Polling stopped")


if __name__ == "__main__":
    asyncio.run(async_main())
