import logging

from application.use_cases import EnsureUserUseCase
from application.use_cases.ensure_user import EnsureUserRequest
from domain.entities.user import User
from infrastructure.cache import Cache
from presentation.common import Messages
from presentation.vk.sdk.types import VkMessage
from presentation.vk.types import UserContext

from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.api import VkSdk

logger = logging.getLogger(__name__)

_CACHE_KEY = "vk:user:{external_id}"
_CACHE_TTL = 86_400


class AuthUserMiddleware:
    def __init__(
        self, vk_sdk: VkSdk, use_case: EnsureUserUseCase, cache: Cache
    ) -> None:
        self._api = vk_sdk
        self._use_case = use_case
        self._cache = cache

    async def __call__(self, message: VkMessage) -> UserContext:

        try:
            key = _CACHE_KEY.format(external_id=message.from_user.id)
            cached_user = await self._cache.get(key)

            if cached_user:
                logger.debug(
                    "AuthUserMiddleware: user %d is cached", message.from_user.id
                )
                user = User.from_dict(cached_user)
                return UserContext(user=user, is_existing=True)

            vk_user = await self._api.get_user_by_id(message.from_user.id)

            response = await self._use_case.execute(
                EnsureUserRequest(
                    external_user_id=str(message.from_user.id),
                    platform="vk",
                    full_name=vk_user.full_name if vk_user else "Пользователь",
                    username=f"id{message.from_user.id}",
                )
            )

            user_ctx = UserContext(user=response.user, is_existing=response.is_existing)
            await self._cache.set(key, user_ctx.user.to_dict(), ttl=_CACHE_TTL)

            return user_ctx
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
