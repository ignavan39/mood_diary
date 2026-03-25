import logging
from typing import TYPE_CHECKING, ClassVar

from application.use_cases import RegisterUserUseCase
from application.use_cases.register_user import RegisterUserRequest
from presentation.common import Messages
from presentation.vk.handlers.base import VkHandler
from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.types import VkMessage

if TYPE_CHECKING:
    from vk_api import VkApi
    from infrastructure import AppContainer

logger = logging.getLogger(__name__)


class RegisterUserHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = (
        "/start",
        "начало",
        "старт",
        "привет",
        "start",
        "hi",
        "hello",
        "здравствуйте",
        "добрый день",
    )

    def __init__(
        self,
        vk_api: "VkApi",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        super().__init__(vk_api, container, group_id)
        self._register_use_case: RegisterUserUseCase = container.services.register_user_use_case()
        

    async def handle(self, message: VkMessage) -> bool:
        if not self._matches_command(message.text):
            return False

        logger.info("VK /start from user %d", message.from_user.id)

        try:
            full_name = await self._get_user_full_name(message.from_user.id)

            response = await self._register_use_case.execute(
                RegisterUserRequest(
                    external_user_id=str(message.from_user.id),
                    platform="vk",
                    full_name=full_name,
                    username=f"id{message.from_user.id}",
                )
            )

            text = (
                Messages.format(
                    Messages.WELCOME_TEXT_FOR_REGISTERED_USER,
                    full_name=full_name,
                )
                if response.is_existing
                else Messages.format(Messages.WELCOME_TEXT, full_name=full_name)
            )

            await self._send_message(
                user_id=message.from_user.id,
                text=text,
                keyboard=kb_main(),
            )

            return True

        except Exception as e:
            logger.exception("StartHandler error for user %d,%e", message.from_user.id, e)
            await self._send_message(
                user_id=message.from_user.id,
                text=Messages.ERROR_GENERIC,
                keyboard=kb_main(),
            )
            return True

    async def _get_user_full_name(self, user_id: int) -> str:
        import asyncio

        def _sync_fetch() -> str:
            users = self._vk.method("users.get", {"user_ids": [user_id]})
            if users:
                u = users[0]
                return f"{u.get('first_name', '')} {u.get('last_name', '')}".strip()
            return "Пользователь"

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _sync_fetch)




__all__ = ["RegisterUserHandler"]
