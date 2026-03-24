import logging

from vkbottle import API, Bot
from vkbottle.bot import Message

from application.use_cases import RegisterUserUseCase
from infrastructure import AppContainer
from presentation.vk.endpoints.user.controllers import RegisterUserController


logger = logging.getLogger(__name__)
 
 
def register_user_handlers(
    bot: Bot,
    api: API,
    container: "AppContainer",
) -> None:
 
    @bot.on.private_message(text=["начало", "/start", "старт", "привет", "start"])
    async def on_start(message: Message) -> None:
        use_case: RegisterUserUseCase = (
            container.services.register_user_use_case.provider()
        )
        await RegisterUserController(use_case, api).call(message)
 