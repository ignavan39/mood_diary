from aiogram.types import Message

from presintation.telegram.endpoints.user.keyboards import (
    create_mood_stats_period_keyboard,
)


class ProfileController:
    async def call(self, message: Message) -> None:
        if message.from_user is None:
            return

        await message.answer(
            "📊 Выберите период для статистики \n\nЗа какой период показать данные?",
            reply_markup=create_mood_stats_period_keyboard().as_markup(),
        )
