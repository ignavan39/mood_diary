from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from presintation.common import Messages


router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(Messages.HELP_TEXT)
