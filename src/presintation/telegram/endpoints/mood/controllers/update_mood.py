import datetime
import logging

from aiogram.types import CallbackQuery

from application.use_cases.update_mood import UpdateMoodRequest, UpdateMoodUseCase
from presintation.common import Messages
from presintation.telegram.endpoints.mood.router import FSMContext
from presintation.telegram.utils import get_mood_emoji

logger = logging.getLogger(__name__)


class UpdateMoodController:
    def __init__(self, use_case: UpdateMoodUseCase) -> None:
        self._use_case = use_case

    async def call(self, query: CallbackQuery, state: FSMContext):
        if query.from_user is None or query.data is None:
            return
        try:
            parts = query.data.split("_")
            diary_id = int(parts[2])
            new_mood = int(parts[3])

            request = UpdateMoodRequest(
                diary_id=diary_id, new_rating=new_mood, date=datetime.date.today()
            )
            response = await self._use_case.execute(request)

            await state.clear()

            emoji = get_mood_emoji(new_mood)
            text = Messages.format(
                Messages.MOOD_UPDATED,
                old_rating=response.old_rating,
                new_rating=response.new_rating,
                emoji=emoji,
            )
            await query.message.edit_text(  # type: ignore
                text
            )
            await query.answer()

        except Exception as e:
            logger.exception("Error in update: %s", e)
            await query.answer(Messages.ERROR_GENERIC, show_alert=True)
