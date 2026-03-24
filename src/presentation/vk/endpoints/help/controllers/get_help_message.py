from vkbottle.bot import Message

from presentation.common.messages import Messages
from presentation.vk.keyboards.main_menu import kb_main


class GetHelpController:
    async def call(self, message: Message) -> None:
        await message.answer(Messages.HELP_TEXT, keyboard=kb_main())
