from aiogram.types import BotCommand

from presintation.common import Messages


commands = [
    BotCommand(command="start", description=Messages.BTN_MAIN_MENU),
    BotCommand(command="mood", description=Messages.BTN_MOOD),
    BotCommand(command="profile", description=Messages.BTN_PROFILE),
    BotCommand(command="help", description=Messages.BTN_HELP),
    BotCommand(command="export", description=Messages.BTN_EXPORT_INFORGRAPHIC),
]
