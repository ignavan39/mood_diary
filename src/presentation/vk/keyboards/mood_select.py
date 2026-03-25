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
