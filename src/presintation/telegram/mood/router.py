from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from presintation.telegram.mood.controllers import GetMenuController


router = Router()


@router.message(Command("mood"))
async def get_menu(
    message: Message,
) -> None:
    controller = GetMenuController()
    await controller.call(message)
