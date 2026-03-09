from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_record_mood_keyboard() -> InlineKeyboardBuilder:
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

    return builder
