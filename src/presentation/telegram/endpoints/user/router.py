from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide, inject

from application.use_cases import (
    EnsureUserUseCase,
    GetUserProfileUseCase,
)
from infrastructure.ioc.container.application import AppContainer
from presentation.telegram.endpoints.user.controllers import RegisterUserController
from presentation.telegram.endpoints.user.controllers.profile import ProfileController


router = Router()


@router.message(Command("start"))
@inject
async def registration(
    message: Message,
    use_case_factory: Factory[EnsureUserUseCase] = Provide[
        AppContainer.services.ensure_user_use_case
    ],
) -> None:
    use_case = use_case_factory.provider()
    await RegisterUserController(use_case).call(message)


@router.message(Command("profile"))
@inject
async def cmd_profile(
    message: Message,
    use_case_factory: Factory[GetUserProfileUseCase] = Provide[
        AppContainer.services.get_user_stats_use_case
    ],
) -> None:
    use_case = use_case_factory.provider()
    await ProfileController(use_case).call(message)


@router.callback_query(F.data.startswith("stats_"))
@inject
async def handle_stats_period(
    callback: CallbackQuery,
    use_case_factory: Factory[GetUserProfileUseCase] = Provide[
        AppContainer.services.get_user_stats_use_case
    ],
) -> None:
    use_case = use_case_factory.provider()
    await ProfileController(use_case).handle_stats_period(callback)
