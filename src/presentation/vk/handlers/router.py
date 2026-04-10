import logging
from typing import TYPE_CHECKING

from presentation.vk.handlers.base import VkHandler
from presentation.vk.handlers.help import GetHelpMessageHandler
from presentation.vk.handlers.mood import (
    GetMoodMenuHandler,
    RecordMoodHandler,
    UpdateMoodHandler,
)
from presentation.vk.handlers.stats import ExportInfographicHandler
from presentation.vk.handlers.user import (
    FallbackHandler,
    GetPofileMenuHandler,
    GetProfileHandler,
    RegisterUserHandler,
)
from presentation.vk.middlewars import AuthUserMiddleware
from presentation.vk.sdk.api import VkSdk
from presentation.vk.sdk.types import VkMessage
from presentation.vk.types import Context

if TYPE_CHECKING:
    from infrastructure import AppContainer

logger = logging.getLogger(__name__)


class VkRouter:
    def __init__(
        self,
        vk_api: "VkSdk",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        self._auth_middleware = AuthUserMiddleware(
            vk_sdk=vk_api,
            use_case=container.services.ensure_user_use_case(),
            cache=container.infrastructure.cache(),
        )
        self._handlers: list[VkHandler] = self._build_handlers(
            vk_api, container, group_id
        )
        logger.info("VkRouter initialized with %d handlers", len(self._handlers))

    @staticmethod
    def _build_handlers(
        vk_api: "VkSdk",
        container: "AppContainer",
        group_id: int,
    ) -> list[VkHandler]:
        return [
            GetProfileHandler(vk_api=vk_api, container=container, group_id=group_id),
            GetHelpMessageHandler(
                vk_api=vk_api, container=container, group_id=group_id
            ),
            GetPofileMenuHandler(vk_api, container, group_id),
            GetMoodMenuHandler(vk_api, container, group_id),
            RecordMoodHandler(vk_api, container, group_id),
            RegisterUserHandler(vk_api, container, group_id),
            UpdateMoodHandler(vk_api, container, group_id),
            ExportInfographicHandler(vk_api, container, group_id),
            FallbackHandler(vk_api, container, group_id),
        ]

    async def route(self, message: VkMessage) -> bool:
        logger.debug(
            "Routing message from %d: '%s'",
            message.from_user.id,
            message.text[:50],
        )

        user_ctx = await self._auth_middleware(message)
        ctx: Context = Context(user_ctx=user_ctx)
        for handler in self._handlers:
            try:
                if await handler.handle_with_metrics(message, ctx):
                    logger.debug("Handled by %s", handler.__class__.__name__)
                    return True
            except Exception as e:
                logger.exception(
                    "Handler %s raised an exception: %s",
                    handler.__class__.__name__,
                    e,
                )
        logger.warning("No handler matched message from %d", message.from_user.id)
        return False


def create_vk_router(
    vk_api: "VkSdk",
    container: "AppContainer",
    group_id: int,
) -> VkRouter:
    return VkRouter(vk_api, container, group_id)


__all__ = ["VkRouter", "create_vk_router"]
