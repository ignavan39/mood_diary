from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.entities import StatsPeriod, periods


def create_mood_stats_period_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for period in periods:
        builder.button(
            text=period.label,
            callback_data=period.callback_data,
        )

    builder.adjust(2, 2, 2)
    return builder


def create_mood_stats_with_refresh_keyboard(
    selected_period: StatsPeriod,
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for period in periods:
        prefix = "✅ " if period == selected_period else "📅 "
        builder.button(
            text=f"{prefix}{period.label}",
            callback_data=period.callback_data,
        )

    builder.adjust(2, 2, 2)
    return builder
