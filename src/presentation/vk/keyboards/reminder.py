from presentation.vk.sdk.keyboards import VkKeyboard, ButtonColor
from presentation.common.messages import Messages


def kb_reminder_hours() -> str:
    keyboard = VkKeyboard(inline=False)

    for hour in range(6, 12):
        keyboard.add_text(f"🌅 {hour:02d}:00", color=ButtonColor.PRIMARY)
        if (hour - 6 + 1) % 3 == 0:
            keyboard.row()

    for hour in range(12, 18):
        keyboard.add_text(f"☀️ {hour:02d}:00", color=ButtonColor.SECONDARY)
        if (hour - 12 + 1) % 3 == 0:
            keyboard.row()

    for hour in range(18, 24):
        keyboard.add_text(f"🌙 {hour:02d}:00", color=ButtonColor.POSITIVE)
        if (hour - 18 + 1) % 3 == 0:
            keyboard.row()

    keyboard.row()
    keyboard.add_text(Messages.REMINDER_DISABLE_TEXT, color=ButtonColor.NEGATIVE)
    keyboard.add_text(Messages.BTN_BACK, color=ButtonColor.SECONDARY)

    return keyboard.to_json()


def kb_reminder_status(enabled: bool, current_hour: int | None) -> str:
    keyboard = VkKeyboard(inline=False)

    if enabled and current_hour is not None:
        text_edit = Messages.REMINDER_EDIT_TEXT.format(current=f"{current_hour:02d}:00")
        keyboard.add_text(text_edit, color=ButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add_text(Messages.REMINDER_DISABLE_TEXT, color=ButtonColor.SECONDARY)
    else:
        keyboard.add_text(Messages.REMINDER_ENABLE_TEXT, color=ButtonColor.POSITIVE)

    keyboard.row()
    keyboard.add_text(Messages.BTN_BACK, color=ButtonColor.SECONDARY)

    return keyboard.to_json()
