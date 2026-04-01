from typing import ClassVar

from presentation.common import Messages
from presentation.vk.handlers.base import VkHandler
from presentation.vk.keyboards import kb_mood_select
from presentation.vk.sdk.types import VkMessage
from presentation.vk.types import Context


class GetMoodMenuHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = (
        Messages.BTN_MOOD,
        "/mood",
        "mood",
        "настроение",
        "оценить",
    )

    async def handle(self, message: VkMessage, ctx: Context) -> bool:
        if not self._matches_command(message.text):
            return False

        await self._api.send_message(
            user_id=message.from_user.id,
            text=Messages.MOOD_QUESTION,
            keyboard=kb_mood_select(),
        )
        return True
