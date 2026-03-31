import logging
from typing import TYPE_CHECKING, ClassVar

from application.use_cases import EnsureUserUseCase
from presentation.common import Messages
from presentation.vk.handlers.base import VkHandler, VkSdk
from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.types import VkMessage
from presentation.vk.types import Context

if TYPE_CHECKING:
    from infrastructure import AppContainer

logger = logging.getLogger(__name__)


class RegisterUserHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = (
        "/start",
        "начало",
        "начать",
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
        vk_api: "VkSdk",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        super().__init__(vk_api, container, group_id)
        self._register_use_case: EnsureUserUseCase = (
            container.services.ensure_user_use_case()
        )

    async def handle(self, message: VkMessage, ctx: Context) -> bool:
        if not self._matches_command(message.text.lower()):
            return False

        logger.info("VK /start from user %d", message.from_user.id)

        try:
            user = ctx.user_ctx.user
            is_existing = ctx.user_ctx.is_existing
            text = (
                Messages.format(
                    Messages.WELCOME_TEXT_FOR_REGISTERED_USER,
                    full_name=user.full_name,
                )
                if is_existing
                else Messages.format(Messages.WELCOME_TEXT, full_name=user.full_name)
            )

            await self._api.send_message(
                user_id=message.from_user.id,
                text=text,
                keyboard=kb_main(),
            )

            return True

        except Exception as e:
            logger.exception(
                "StartHandler error for user %d,%e", message.from_user.id, e
            )
            await self._api.send_message(
                user_id=message.from_user.id,
                text=Messages.ERROR_GENERIC,
                keyboard=kb_main(),
            )
            return True

    async def _get_user_full_name(self, user_id: int) -> str:
        user = await self._api.get_user_by_id(user_id)
        return user.full_name if user else "Пользователь"


__all__ = ["RegisterUserHandler"]
