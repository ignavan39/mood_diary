from presentation.common import Messages
from presentation.vk.sdk.keyboards import ButtonColor, VkKeyboard


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
