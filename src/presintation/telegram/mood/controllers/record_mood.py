from datetime import datetime

from aiogram.types import CallbackQuery

from application.use_cases import RecordMoodUseCase
from application.use_cases.record_mood import RecordMoodRequest


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
            user_id = query.from_user.id

            request = RecordMoodRequest(
                external_user_id=user_id, rating=mood_value, date=datetime.now().date()
            )
            await self._use_case.execute(request)

            emoji = get_mood_emoji(mood_value)
            await query.message.edit_text( # type: ignore
                f"{emoji} Настроение сохранено!\n\n"
                f"Твоя оценка: {mood_value}/10\n\n"
                f"Используй /profile чтобы посмотреть статистику."
            )

            await query.answer()

        except ValueError:
            await query.answer("❌ Неверное значение", show_alert=True)
        except Exception:
            await query.answer("⚠️ Ошибка. Попробуйте позже.", show_alert=True)


def get_mood_emoji(value: int) -> str:
    if value <= 2:
        return "😢"
    elif value <= 4:
        return "😟"
    elif value <= 6:
        return "😐"
    elif value <= 8:
        return "🙂"
    else:
        return "😄"
