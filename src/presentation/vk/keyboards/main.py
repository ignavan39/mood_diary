from presentation.common import Messages
from presentation.vk.sdk.keyboards import ButtonColor, VkKeyboard


def kb_main() -> str:
    return (
        VkKeyboard(one_time=False, inline=False)
        .add_text(Messages.BTN_MOOD, color=ButtonColor.POSITIVE)
        .add_text(Messages.BTN_PROFILE, color=ButtonColor.PRIMARY)
        .row()
        .add_text(Messages.BTN_EXPORT_INFORGRAPHIC, color=ButtonColor.SECONDARY)
        .add_text(Messages.BTN_HELP, color=ButtonColor.SECONDARY)
        .to_json()
    )
