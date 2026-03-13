import logging

from aiogram.types import Message

from application.use_cases import RegisterUserRequest, RegisterUserUseCase
from infrastructure.metrics import messages_total

logger = logging.getLogger(__name__)


class RegisterUserController:
    def __init__(self, use_case: RegisterUserUseCase):
        self._use_case = use_case

    async def call(self, message: Message) -> None:
        if message.from_user is None:
            return
        try:
            tg_id = message.from_user.id
            full_name = message.from_user.full_name or "Пользователь"
            username = message.from_user.username or "Пользователь"

            request = RegisterUserRequest(
                external_user_id=str(tg_id),
                full_name=full_name,
                platform="telegram",
                username=username,
            )
            response = await self._use_case.execute(request)
            messages_total.labels(command="start", status="success").inc()

            if response.is_existing:
                await message.answer(
                    f"✅ С возвращением, {full_name}!\n\n"
                    f"Используй /mood чтобы отметить настроение."
                )
            else:
                await message.answer(
                    f"👋Привет, {full_name}!\n\n"
                    f"Я помогу тебе отслеживать настроение.\n"
                    f"Используй /mood чтобы оценить своё состояние."
                )
        except Exception as e:
            logger.error("Error in /start: %s", e)
            messages_total.labels(command="start", status="error").inc()
            await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")
