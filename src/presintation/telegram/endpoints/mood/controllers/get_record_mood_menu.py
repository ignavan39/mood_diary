from aiogram.types import Message

from presintation.telegram.endpoints.mood.keyboards import create_record_mood_keyboard


class GetRecordMoodMenuController:
    async def call(self, message: Message):
        if message.from_user is None:
            return

        builder = create_record_mood_keyboard()

        await message.answer(
            "Как твоё настроение?\n\n"
            "Выберите значение от 0 до 10:\n"
            "0 = Очень плохо, 10 = Отлично",
            reply_markup=builder.as_markup(),
        )
