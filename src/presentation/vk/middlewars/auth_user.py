import logging

from application.use_cases import EnsureUserUseCase
from application.use_cases.ensure_user import EnsureUserRequest
from infrastructure.cache import Cache
from presentation.common import Messages
from presentation.vk.sdk.types import VkMessage
from presentation.vk.types import UserContext

from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.api import VkSdk

logger = logging.getLogger(__name__)


class AuthUserMiddleware:
    def __init__(
        self, vk_sdk: VkSdk, use_case: EnsureUserUseCase, cache: Cache
    ) -> None:
        self._api = vk_sdk
        self._use_case = use_case
        self._cache = cache

    async def __call__(self, message: VkMessage) -> UserContext:

        try:
            vk_user = await self._api.get_user_by_id(message.from_user.id)

            response = await self._use_case.execute(
                EnsureUserRequest(
                    external_user_id=str(message.from_user.id),
                    platform="vk",
                    full_name=vk_user.full_name if vk_user else "Пользователь",
                    username=f"id{message.from_user.id}",
                )
            )

            return UserContext(user=response.user, is_existing=response.is_existing)
        except Exception as e:
            logger.exception(
                "AuthUserMiddleware error for user %d,%e", message.from_user.id, e
            )
            await self._api.send_message(
                user_id=message.from_user.id,
                text=Messages.ERROR_GENERIC,
                keyboard=kb_main(),
            )
            raise e
