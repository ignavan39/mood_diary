import asyncio
import logging

from aiogram import Bot, Dispatcher

from application.use_cases import RegisterUserUseCase
from domain.entities import User
from domain.exceptions import DuplicateUserError
from infrastructure.configs import settings
from infrastructure.database.repositories import SQLAchemyUserRepository
from infrastructure.database import sessionmanager
from infrastructure.telegram.handlers.user import create_user_handler

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    me = await bot.get_me()
    logger.info(f"🤖 Bot started: @{me.username}")


async def on_shutdown(bot: Bot):
    logger.info("🛑 Bot stopped")
    await bot.session.close()
    await sessionmanager.close()


async def async_main() -> None:
    bot = Bot(settings.tg_bot.token)

    dp = Dispatcher()
    async with sessionmanager.session() as session:
        logger.info("Starting mood_diary bot...")

        repo = SQLAchemyUserRepository(session)
        register_user_uc = RegisterUserUseCase(repo)

        create_user_handler(router=dp, register_user_uc=register_user_uc)
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(async_main())
