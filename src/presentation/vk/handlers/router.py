import logging
from typing import TYPE_CHECKING

from presentation.vk.handlers.base import VkHandler
from presentation.vk.handlers.help import GetHelpMessageHandler
from presentation.vk.handlers.user import GetPofileMenuHandler, GetProfileHandler
from presentation.vk.handlers.user.fallback import FallbackHandler
from presentation.vk.handlers.user.register import RegisterUserHandler
from presentation.vk.sdk.types import VkMessage

if TYPE_CHECKING:
    from vk_api import VkApi
    from infrastructure import AppContainer

logger = logging.getLogger(__name__)


class VkRouter:
    def __init__(
        self,
        vk_api: "VkApi",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        self._handlers: list[VkHandler] = self._build_handlers(
            vk_api, container, group_id
        )
        logger.info("VkRouter initialized with %d handlers", len(self._handlers))

    @staticmethod
    def _build_handlers(
        vk_api: "VkApi",
        container: "AppContainer",
        group_id: int,
    ) -> list[VkHandler]:
        kwargs = {"vk_api": vk_api, "container": container, "group_id": group_id}
        return [
            GetProfileHandler(**kwargs),
            RegisterUserHandler(**kwargs),
            GetHelpMessageHandler(**kwargs),
            GetPofileMenuHandler(**kwargs),
            FallbackHandler(**kwargs),
        ]

    async def route(self, message: VkMessage) -> bool:
        logger.debug(
            "Routing message from %d: '%s'",
            message.from_user.id,
            message.text[:50],
        )
        for handler in self._handlers:
            try:
                if await handler.handle(message):
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
    vk_api: "VkApi",
    container: "AppContainer",
    group_id: int,
) -> VkRouter:
    return VkRouter(vk_api, container, group_id)


__all__ = ["VkRouter", "create_vk_router"]
