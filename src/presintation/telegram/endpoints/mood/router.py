from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide, inject

from application.use_cases import RecordMoodUseCase
from application.use_cases.update_mood import UpdateMoodUseCase
from infrastructure.ioc.container.application import AppContainer
from presintation.telegram.endpoints.mood.controllers import (
    GetRecordMoodMenuController,
    RecordMoodController,
    UpdateMoodController,
)


router = Router()


@router.message(Command("mood"))
async def get_menu(
    message: Message,
) -> None:
    controller = GetRecordMoodMenuController()
    await controller.call(message)


@router.callback_query(F.data.startswith("mood_"))
async def record_mood(
    callback: CallbackQuery,
    use_case_factory: Factory[RecordMoodUseCase] = Provide[
        AppContainer.services.record_mood_use_case
    ],
) -> None:
    use_case: RecordMoodUseCase = use_case_factory.provider()
    return await RecordMoodController(use_case).call(callback)


@router.callback_query(F.data.startswith("update_yes_"))
@inject
async def handle_update_confirmed(
    callback: CallbackQuery,
    use_case_factory: Factory[UpdateMoodUseCase] = Provide[
        AppContainer.services.update_mood_use_case
    ],
) -> None:
    use_case: UpdateMoodUseCase = use_case_factory.provider()
    return await UpdateMoodController(use_case).call(callback)
