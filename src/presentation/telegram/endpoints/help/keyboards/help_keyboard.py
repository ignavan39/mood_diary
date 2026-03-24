from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from presentation.common import Messages


def create_help_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=Messages.BTN_MOOD, callback_data="cmd_mood")
    builder.button(text=Messages.BTN_PROFILE, callback_data="cmd_profile")
    builder.button(text=Messages.BTN_MAIN_MENU, callback_data="cmd_start")

    builder.adjust(2, 1)
    return builder.as_markup()
