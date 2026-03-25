from presentation.common import Messages
from presentation.vk.sdk.keyboards import ButtonColor, VkKeyboard


def kb_mood_select() -> str:
    keyboard = VkKeyboard(inline=True)

    for i in range(10, 7, -1):
        keyboard.add_callback(
            label=str(i),
            color=ButtonColor.POSITIVE,
            payload={"mood": str(i)},
        )
    keyboard.row()

    for i in range(7, 4, -1):
        keyboard.add_callback(
            label=str(i),
            color=ButtonColor.PRIMARY,
            payload={"mood": str(i)},
        )
    keyboard.row()

    for i in range(4, 0, -1):
        keyboard.add_callback(
            label=str(i),
            color=ButtonColor.NEGATIVE if i <= 2 else ButtonColor.SECONDARY,
            payload={"mood": str(i)},
        )
    keyboard.row()

    keyboard.add_callback(Messages.BTN_CANCEL, color=ButtonColor.NEGATIVE)

    return keyboard.to_json()


def kb_profile() -> str:
    return (
        VkKeyboard(inline=True)
        .add_text(Messages.BTN_MOOD, color=ButtonColor.POSITIVE)
        .add_text(Messages.BTN_EXPORT_INFORGRAPHIC, color=ButtonColor.PRIMARY)
        .row()
        .add_callback(Messages.BTN_BACK, payload={"action": "back_to_menu"})
        .to_json()
    )


def kb_confirm(
    confirm_text: str = Messages.BTN_YES,
    cancel_text: str = Messages.BTN_NO,
    confirm_payload: dict[str, str] | None = None,
    cancel_payload: dict[str, str] | None = None,
) -> str:
    return (
        VkKeyboard(inline=True)
        .add_callback(confirm_text, color=ButtonColor.POSITIVE, payload=confirm_payload)
        .add_callback(cancel_text, color=ButtonColor.NEGATIVE, payload=cancel_payload)
        .to_json()
    )


def kb_back(label: str = Messages.BTN_BACK) -> str:
    return (
        VkKeyboard(inline=True)
        .add_callback(label, color=ButtonColor.SECONDARY)
        .to_json()
    )
