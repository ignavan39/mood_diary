from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.dtos import StatsPeriod


def create_mood_stats_period_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    periods = [
        StatsPeriod.WEEK,
        StatsPeriod.MONTH,
        StatsPeriod.QUARTER,
        StatsPeriod.HALF_YEAR,
        StatsPeriod.YEAR,
        StatsPeriod.ALL,
    ]

    for period in periods:
        builder.button(
            text=period.label,
            callback_data=period.callback_data,
        )

    builder.adjust(2, 2, 2)
    return builder
