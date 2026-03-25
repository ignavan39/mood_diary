import logging
from typing import ClassVar
from presentation.common import Messages
from presentation.vk.handlers.base import VkHandler
from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.types import VkMessage

logger = logging.getLogger(__name__)


class FallbackHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = ()

    async def handle(self, message: VkMessage) -> bool:
        if not message.text.strip():
            return False

        logger.debug(
            "Fallback: unhandled message from %d: %s",
            message.from_user.id,
            message.text[:50],
        )

        await self._send_message(
            user_id=message.from_user.id,
            text=Messages.WELCOME_STUB_MESSAGE,
            keyboard=kb_main(),
        )

        return True
