from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide, inject

from application.use_cases import RegisterUserUseCase
from infrastructure.ioc.container.application import AppContainer
from presintation.telegram.user.controllers import RegisterUserController


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
