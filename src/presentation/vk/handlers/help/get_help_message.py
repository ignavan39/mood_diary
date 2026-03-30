import logging
from typing import ClassVar

from presentation.common.messages import Messages
from presentation.vk.handlers.base import VkHandler
from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.types import VkMessage

logger = logging.getLogger(__name__)


class GetHelpMessageHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = (
        Messages.BTN_HELP,
        "/help",
        "help",
        "помощь",
    )

    async def handle(self, message: VkMessage) -> bool:
        if not self._matches_command(message.text.lower()):
            return False

        text = Messages.HELP_TEXT
        await self._send_message(
            user_id=message.from_user.id,
            text=text,
            keyboard=kb_main(),
        )
        return True
