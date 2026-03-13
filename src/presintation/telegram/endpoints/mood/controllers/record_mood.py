from datetime import date, datetime
import logging

from aiogram.types import CallbackQuery

from application.use_cases import RecordMoodUseCase
from application.use_cases.record_mood import RecordMoodRequest
from aiogram.fsm.context import FSMContext

from domain.exceptions import InvalidDiaryRatingError
from presintation.telegram.endpoints.mood.keyboards import (
    create_update_confirmation_keyboard,
)
from presintation.telegram.endpoints.mood.states import MoodFlow
from presintation.telegram.utils import get_mood_emoji

logger = logging.getLogger(__name__)


class RecordMoodController:
    def __init__(self, use_case: RecordMoodUseCase) -> None:
        self._use_case = use_case

    async def call(self, query: CallbackQuery, state: FSMContext):
        if query.from_user is None:
            return
        err_str = "❌ Неверное значение, значение должно быть в диапазоне от 1 до 10"
        try:
            if query.data is None:
                return

            if query.message is None:
                return

            mood_value = int(query.data.split("_")[1])

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

                await state.update_data(existing_diary_id=exist_diary.existing_diary_id)
                await state.set_state(MoodFlow.confirming_update)

                emoji = get_mood_emoji(mood_value)
                await query.message.edit_text(  # type: ignore
                    f"⚠️Запись за {today.strftime('%d.%m')} уже есть!\n\n"
                    f"Текущая: {exist_diary.old_rating}/10\n"
                    f"Новая: {emoji} {mood_value}/10\n\n"
                    f"Хотите обновить?",
                    reply_markup=create_update_confirmation_keyboard(
                        diary_id=exist_diary.existing_diary_id,
                        new_rating=mood_value,
                    ).as_markup(),
                )
            else:
                await state.clear()
                emoji = get_mood_emoji(mood_value)
                await query.message.edit_text(  # type: ignore
                    f"{emoji} Настроение сохранено!\n\n"
                    f"Твоя оценка: {mood_value}/10\n\n"
                    f"Используй /profile чтобы посмотреть статистику."
                )

            await query.answer()

        except ValueError:
            await query.answer(err_str, show_alert=True)
        except InvalidDiaryRatingError:
            await query.answer(err_str, show_alert=True)
        except Exception as e:
            logger.exception("Error in mood selection %s", e)
            await query.answer("⚠️ Ошибка. Попробуйте позже.", show_alert=True)
