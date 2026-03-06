from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide

from application.use_cases import RecordMoodUseCase
from infrastructure.ioc.container.application import AppContainer
from presintation.telegram.mood.controllers import (
    GetMenuController,
    RecordMoodController,
)


router = Router()


@router.message(Command("mood"))
async def get_menu(
    message: Message,
) -> None:
    controller = GetMenuController()
    await controller.call(message)


@router.callback_query(F.data.startswith("mood_"))
async def recoed_modd(
    callback: CallbackQuery,
    use_case_factory: Factory[RecordMoodUseCase] = Provide[
        AppContainer.services.record_mood_use_case
    ],
) -> None:
    use_case = use_case_factory.provider()
    return await RecordMoodController(use_case).call(callback)
