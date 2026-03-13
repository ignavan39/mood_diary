from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_help_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🎯 Оценить настроение", callback_data="cmd_mood")
    builder.button(text="📊 Статистика", callback_data="cmd_profile")
    builder.button(text="🏠 Главное меню", callback_data="cmd_start")

    builder.adjust(2, 1)
    return builder.as_markup()
