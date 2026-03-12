from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide, inject

from application.use_cases import GetUserStatsUseCase, RegisterUserUseCase
from infrastructure.ioc.container.application import AppContainer
from presintation.telegram.endpoints.user.controllers import RegisterUserController
from presintation.telegram.endpoints.user.controllers.profile import ProfileController
from presintation.telegram.endpoints.user.states import StatsFlow


router = Router()


@router.message(Command("start"))
@inject
async def registration(
    message: Message,
    use_case_factory: Factory[RegisterUserUseCase] = Provide[
        AppContainer.services.register_user_use_case
    ],
) -> None:
    use_case = use_case_factory.provider()
    await RegisterUserController(use_case).call(message)


@router.message(Command("profile"))
@inject
async def cmd_profile(
    message: Message,
    state: FSMContext,
    use_case_factory: Factory[GetUserStatsUseCase] = Provide[
        AppContainer.services.get_user_stats_use_case
    ],
) -> None:
    use_case = use_case_factory.provider()
    await ProfileController(use_case).call(message, state)


@router.callback_query(F.data.startswith("stats_"), StatsFlow.viewing_stats)
@inject
async def handle_stats_period(
    callback: CallbackQuery,
    use_case_factory: Factory[GetUserStatsUseCase] = Provide[
        AppContainer.services.get_user_stats_use_case
    ],
) -> None:
    use_case = use_case_factory.provider()
    await ProfileController(use_case).handle_stats_period(callback)
