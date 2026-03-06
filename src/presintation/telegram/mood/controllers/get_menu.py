from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


class GetMenuController:
    async def call(self, message: Message):
        if message.from_user is None:
            return

        builder = InlineKeyboardBuilder()

        mood_emojis = {
            0: "😢",
            1: "😢",
            2: "😟",
            3: "😟",
            4: "😕",
            5: "😐",
            6: "🙂",
            7: "🙂",
            8: "😊",
            9: "😄",
            10: "😄",
        }

        for i in range(0, 11):
            emoji = mood_emojis.get(i, "😐")
            builder.button(text=f"{emoji} {i}", callback_data=f"mood_{i}")

        builder.adjust(6, 5)

        await message.answer(
            "Как твоё настроение?\n\n"
            "Выберите значение от 0 до 10:\n"
            "0 = Очень плохо, 10 = Отлично",
            reply_markup=builder.as_markup(),
        )
