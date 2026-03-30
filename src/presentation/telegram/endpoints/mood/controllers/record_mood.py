from datetime import date, datetime
import logging

from aiogram.types import CallbackQuery

from application.use_cases import RecordMoodUseCase
from application.use_cases.record_mood import RecordMoodRequest

from domain.exceptions import InvalidDiaryRatingError
from presentation.common import Messages
from presentation.telegram.endpoints.mood.keyboards import (
    create_update_confirmation_keyboard,
)

logger = logging.getLogger(__name__)


class RecordMoodController:
    def __init__(self, use_case: RecordMoodUseCase) -> None:
        self._use_case = use_case

    async def call(self, query: CallbackQuery):
        if query.from_user is None:
            return
        try:
            if query.data is None:
                return

            if query.message is None:
                return

            mood_value = int(query.data.split("_")[1])
            emoji = Messages.get_mood_emoji(mood_value)

            user_id = query.from_user.id

            request = RecordMoodRequest(
                external_user_id=str(user_id),
                rating=mood_value,
                date=datetime.now().date(),
                platform="telegram",
            )
            response = await self._use_case.execute(request)

            today = date.today()
            logger.info(response)

            if response.needs_confirmation is True and response.exist_diary is not None:
                exist_diary = response.exist_diary
                text = Messages.format(
                    Messages.MOOD_DUPLICATE,
                    today=today.strftime("%d.%m"),
                    old_rating=exist_diary.old_rating,
                    new_rating=mood_value,
                    emoji=emoji,
                    mood=mood_value,
                )
                await query.message.edit_text(  # type: ignore
                    text,
                    reply_markup=create_update_confirmation_keyboard(
                        diary_id=exist_diary.existing_diary_id,
                        new_rating=mood_value,
                    ).as_markup(),
                )
            else:
                text = Messages.format(
                    Messages.MOOD_SAVED,
                    mood=mood_value,
                    emoji=emoji,
                )
                await query.message.edit_text(  # type: ignore
                    text
                )

            await query.answer()

        except ValueError:
            await query.answer(Messages.INVALID_DIARY_RATING, show_alert=True)
        except InvalidDiaryRatingError:
            await query.answer(Messages.INVALID_DIARY_RATING, show_alert=True)
        except Exception as e:
            logger.exception("Error in mood selection %s", e)
            await query.answer(Messages.ERROR_GENERIC, show_alert=True)
