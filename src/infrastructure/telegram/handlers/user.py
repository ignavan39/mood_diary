import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from application.use_cases import RegisterUserRequest, RegisterUserUseCase
from infrastructure.database.repositories import SQLAchemyUserRepository
from infrastructure.database.session_manager import AsyncSession


logger = logging.getLogger(__name__)


class UserHandler:
    def __init__(
        self,
        router: Router,
    ) -> None:
        self.router = router

        self._register_handlers()

    def _register_handlers(self) -> None:
        self.router.message.register(self.cmd_start, Command("start"))

    async def cmd_start(self, message: Message, session: AsyncSession) -> None:
        if message.from_user is None:
            return

        try:
            tg_id = message.from_user.id
            name = message.from_user.full_name or "Пользователь"

            user_repo = SQLAchemyUserRepository(session)
            use_case = RegisterUserUseCase(user_repo)

            request = RegisterUserRequest(
                user_id=tg_id,
                name=name,
            )
            request = RegisterUserRequest(
                user_id=tg_id,
                name=name,
            )
            response = await use_case.execute(request)

            if response.is_existing:
                await message.answer(
                    f"✅ С возвращением, {name}!\n\n"
                    f"Используй /mood чтобы отметить настроение."
                )
            else:
                await message.answer(
                    f"👋Привет, {name}!\n\n"
                    f"Я помогу тебе отслеживать настроение.\n"
                    f"Используй /mood чтобы оценить своё состояние."
                )

        except Exception as e:
            logger.error("Error in /start: %s", e)
            await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")


def create_user_handler(
    router: Router,
) -> UserHandler:
    return UserHandler(
        router=router,
    )
