from vkbottle import Keyboard, KeyboardButtonColor, Text

from presentation.common import Messages


def kb_main() -> str:
    return (
        Keyboard(one_time=False)
        .add(Text(Messages.BTN_MOOD), color=KeyboardButtonColor.POSITIVE)
        .add(Text(Messages.BTN_PROFILE), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(
            Text(Messages.BTN_EXPORT_INFORGRAPHIC), color=KeyboardButtonColor.SECONDARY
        )
        .add(Text(Messages.BTN_HELP), color=KeyboardButtonColor.SECONDARY)
        .get_json()
    )
