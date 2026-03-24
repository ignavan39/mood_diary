from aiogram.types import Message

from presentation.common import Messages
from presentation.telegram.endpoints.mood.keyboards import create_record_mood_keyboard


class GetRecordMoodMenuController:
    async def call(self, message: Message):
        if message.from_user is None:
            return

        builder = create_record_mood_keyboard()

        await message.answer(Messages.MOOD_QUESTION, reply_markup=builder.as_markup())
