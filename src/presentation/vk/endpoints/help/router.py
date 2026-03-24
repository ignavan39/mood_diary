import logging

from vkbottle import Bot
from vkbottle.bot import Message

from presentation.common import Messages
from presentation.vk.endpoints.help.controllers import GetHelpController


logger = logging.getLogger(__name__)


def register_help_handlers(
    bot: Bot,
) -> None:

    @bot.on.private_message(text=[Messages.BTN_HELP, "/help", "help", "помощь"])
    async def get_help_message(message: Message) -> None:
        await GetHelpController().call(message)
