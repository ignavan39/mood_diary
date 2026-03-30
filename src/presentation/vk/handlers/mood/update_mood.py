from datetime import datetime
import logging
from typing import ClassVar

from application.use_cases.update_mood import UpdateMoodRequest, UpdateMoodUseCase
from infrastructure import AppContainer
from presentation.common import Messages
from presentation.vk.handlers.base import VkHandler
from vk_api import VkApi

from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.types import VkMessage

PLATFORM = "vk"


logger = logging.getLogger(__name__)


class UpdateMoodHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = ()

    def __init__(
        self, vk_api: "VkApi", container: "AppContainer", group_id: int
    ) -> None:
        super().__init__(vk_api, container, group_id)
        self._use_case: UpdateMoodUseCase = container.services.update_mood_use_case()

    def matches(self, message: VkMessage) -> bool:
        return message.payload is not None and (
            message.payload.get("action") == "update_mood_yes"
            or message.payload.get("action") == "update_mood_no"
        )

    async def handle(self, message: VkMessage) -> bool:
        if not self.matches(message) or message.payload is None:
            return False

        if message.payload.get("action") == "update_mood_no":
            await self._send_message(
                user_id=message.from_user.id,
                text=Messages.WELCOME_STUB_MESSAGE,
                keyboard=kb_main(),
            )
            return True
        try:
            diary_id = int(message.payload["diary_id"])
            new_rating = int(message.payload["rating"])

            response = await self._use_case.execute(
                UpdateMoodRequest(
                    diary_id=diary_id,
                    new_rating=new_rating,
                    date=datetime.now().date(),
                )
            )
            emoji = Messages.get_mood_emoji(new_rating)

            if response.old_rating == new_rating:
                text = Messages.format(
                    Messages.MOOD_UPDATE_EQUAL, rating=new_rating, emoji=emoji
                )
            else:
                text = Messages.format(
                    Messages.MOOD_UPDATED,
                    emoji=emoji,
                    old_rating=response.old_rating,
                    new_rating=response.new_rating,
                )

            await self._send_message(
                user_id=message.from_user.id,
                text=text,
                keyboard=kb_main(),
            )
            return True

        except Exception as e:
            logger.exception("UpdateMoodHandler error: %s", e)
            await self._send_message(
                user_id=message.from_user.id,
                text=Messages.ERROR_GENERIC,
                keyboard=kb_main(),
            )
            return True
