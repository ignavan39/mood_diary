import logging
from typing import TYPE_CHECKING, ClassVar
from datetime import datetime

from application.use_cases import RecordMoodUseCase
from application.use_cases.record_mood import RecordMoodRequest
from domain.exceptions import UserNotFoundError
from presentation.common import Messages
from presentation.vk.handlers.base import VkHandler
from presentation.vk.keyboards import kb_confirm, kb_main
from presentation.vk.sdk.types import VkMessage

if TYPE_CHECKING:
    from vk_api import VkApi
    from infrastructure import AppContainer

PLATFORM = "vk"
logger = logging.getLogger(__name__)


class RecordMoodHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = ()

    def __init__(
        self,
        vk_api: "VkApi",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        super().__init__(vk_api, container, group_id)
        self._container = container
        self._use_case: RecordMoodUseCase = container.services.record_mood_use_case()

    def _matches_payload(self, message: VkMessage) -> bool:
        if not message.payload:
            return False
        return "mood" in message.payload

    def _matches_text(self, message: VkMessage) -> bool:
        text = message.text.strip()

        if len(text) >= 3 and text[-1].isdigit():
            try:
                value = int(text[-1])
                return 0 <= value <= 10
            except ValueError:
                pass

        if text.isdigit():
            value = int(text)
            return 0 <= value <= 10

        return False

    async def handle(self, message: VkMessage) -> bool:
        logger.debug(
            "RecordMoodHandler checking: text='%s', payload=%s, event_id=%s",
            message.text,
            message.payload,
            message.event_id,
        )

        if self._matches_text(message):
            text = message.text.strip()
            rating = int(text[-1]) if text[-1].isdigit() else int(text)
        else:
            return False

        logger.info("VK mood selection from user %d", message.from_user.id)

        event_id = message.event_id

        try:
            response = await self._use_case.execute(
                RecordMoodRequest(
                    external_user_id=str(message.from_user.id),
                    platform=PLATFORM,
                    rating=rating,
                    date=datetime.now().date(),
                )
            )
            emoji = Messages.get_mood_emoji(rating)

            if response.needs_confirmation and response.exist_diary:
                ed = response.exist_diary
                await self._send_message(
                    user_id=message.from_user.id,
                    text=Messages.format(
                        Messages.MOOD_DUPLICATE,
                        today=datetime.now().strftime("%d.%m"),
                        old_rating=ed.old_rating,
                        new_rating=rating,
                        emoji=emoji,
                        mood=rating,
                    ),
                    keyboard=kb_confirm(
                        confirm_payload={
                            "action": "update_mood",
                            "diary_id": str(ed.existing_diary_id),
                            "rating": str(rating),
                        },
                        cancel_payload={"action": "cancel"},
                    ),
                )
            else:
                await self._send_message(
                    user_id=message.from_user.id,
                    text=Messages.format(Messages.MOOD_SAVED, mood=rating, emoji=emoji),
                    keyboard=kb_main(),
                )

            if event_id:
                await self._answer_callback_event(
                    event_id=event_id,
                    user_id=message.from_user.id,
                    action=None,
                )

            return True

        except UserNotFoundError:
            if event_id:
                await self._answer_callback_event(
                    event_id=event_id,
                    user_id=message.from_user.id,
                    action=None,
                )
            await self._send_message(
                user_id=message.from_user.id,
                text=Messages.WELCOME_STUB_MESSAGE,
                keyboard=kb_main(),
            )
            return True

        except Exception as e:
            logger.exception("RecordMoodHandler error: %s", e)
            if event_id:
                await self._answer_callback_event(
                    event_id=event_id,
                    user_id=message.from_user.id,
                    action=None,
                )
            await self._send_message(
                user_id=message.from_user.id,
                text=Messages.ERROR_GENERIC,
                keyboard=kb_main(),
            )
            return True
