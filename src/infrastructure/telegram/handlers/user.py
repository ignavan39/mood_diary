import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from application.use_cases import RegisterUserRequest, RegisterUserUseCase


logger = logging.getLogger(__name__)


class UserHandler:
    def __init__(
        self,
        router: Router,
        register_user_uc: RegisterUserUseCase,
    ) -> None:
        self.router = router
        self.register_user_uc = register_user_uc

        self._register_handlers()

    def _register_handlers(self) -> None:
        self.router.message.register(self.cmd_start, Command("start"))

    async def cmd_start(self, message: Message) -> None:
        if message.from_user is None:
            return

        telegram_id = message.from_user.id
        name = message.from_user.full_name
        username = message.from_user.username

        logger.info("Processing /start for user %s", telegram_id)

        try:
            request = RegisterUserRequest(
                user_id=telegram_id,
                name=name,
            )
            response = await self.register_user_uc.execute(request)

            if response.is_existing:
                await message.answer(
                    f"✅ <b>С возвращением, {name}!</b>\n\n"
                    f"Используй /mood чтобы отметить настроение."
                )
            else:
                await message.answer(
                    f"👋 <b>Привет, {name}!</b>\n\n"
                    f"Я помогу тебе отслеживать настроение.\n"
                    f"Используй /mood чтобы оценить своё состояние."
                )

        except Exception as e:
            logger.error("Error in /start: %s", e)
            await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")


def create_user_handler(
    router: Router,
    register_user_uc: RegisterUserUseCase,
) -> UserHandler:
    return UserHandler(
        router=router,
        register_user_uc=register_user_uc,
    )