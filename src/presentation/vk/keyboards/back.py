from presentation.common import Messages
from presentation.vk.sdk.keyboards import ButtonColor, VkKeyboard


def kb_back(label: str = Messages.BTN_BACK) -> str:
    return (
        VkKeyboard(inline=True)
        .add_callback(label, color=ButtonColor.SECONDARY)
        .to_json()
    )
