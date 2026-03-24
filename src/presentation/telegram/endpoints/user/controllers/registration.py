import logging

from aiogram.types import Message

from application.use_cases import RegisterUserRequest, RegisterUserUseCase
from presentation.common import Messages

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

            if response.is_existing:
                await message.answer(
                    Messages.format(
                        Messages.WELCOME_TEXT_FOR_REGISTERED_USER, full_name=full_name
                    )
                )
            else:
                await message.answer(
                    Messages.format(Messages.WELCOME_TEXT, full_name=full_name)
                )
        except Exception as e:
            logger.error("Error in /start: %s", e)
            await message.answer(Messages.ERROR_GENERIC)
