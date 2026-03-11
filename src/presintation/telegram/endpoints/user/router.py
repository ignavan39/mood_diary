from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide, inject

from application.use_cases import RegisterUserUseCase
from infrastructure.ioc.container.application import AppContainer
from presintation.telegram.endpoints.user.controllers import RegisterUserController
from presintation.telegram.endpoints.user.keyboards import (
    create_mood_stats_period_keyboard,
)


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
    controller = RegisterUserController(use_case)
    await controller.call(message)


@router.message(Command("profile"))
async def cmd_profile(
    message: Message,
) -> None:
    if message.from_user is None:
        return

    await message.answer(
        "📊 Выберите период для статистики \n\nЗа какой период показать данные?",
        reply_markup=create_mood_stats_period_keyboard().as_markup(),
    )
