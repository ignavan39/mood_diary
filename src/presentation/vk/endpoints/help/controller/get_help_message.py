from vkbottle.bot import Message

from presentation.common.messages import Messages
from presentation.vk.endpoints.help.keyboards import create_help_keyboard


class GetHelpController:
    async def call(self, message: Message) -> None:
        await message.answer(Messages.HELP_TEXT, keyboard=create_help_keyboard())
