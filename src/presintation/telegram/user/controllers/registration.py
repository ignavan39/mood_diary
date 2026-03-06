import logging

from aiogram.types import Message

from application.use_cases import RegisterUserRequest, RegisterUserUseCase

logger = logging.getLogger(__name__)


class RegisterUserController:
    def __init__(self, use_case: RegisterUserUseCase):
        self._use_case = use_case

    async def call(self, message: Message) -> None:
        if message.from_user is None:
            return
        try:
            tg_id = message.from_user.id
            name = message.from_user.full_name or "Пользователь"

            request = RegisterUserRequest(
                user_id=tg_id,
                name=name,
            )
            request = RegisterUserRequest(
                user_id=tg_id,
                name=name,
            )
            response = await self._use_case.execute(request)
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
