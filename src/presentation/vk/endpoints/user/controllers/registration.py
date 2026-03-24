import logging

from vkbottle import API
from vkbottle.bot import Message

from application.use_cases.register_user import RegisterUserRequest, RegisterUserUseCase
from presentation.common import Messages
from presentation.vk.keyboards.main_menu import kb_main

logger = logging.getLogger(__name__)

PLATFORM = "vk"


class RegisterUserController:
    def __init__(self, use_case: RegisterUserUseCase, api: API) -> None:
        self._use_case = use_case
        self._api = api

    async def call(self, message: Message) -> None:
        try:
            vk_users = await self._api.users.get(user_ids=[message.from_id])
            vk_user = vk_users[0]
            full_name = f"{vk_user.first_name} {vk_user.last_name}".strip()

            response = await self._use_case.execute(
                RegisterUserRequest(
                    external_user_id=str(message.from_id),
                    platform=PLATFORM,
                    full_name=full_name,
                    username=str(message.from_id),
                )
            )

            text = (
                Messages.format(
                    Messages.WELCOME_TEXT_FOR_REGISTERED_USER, full_name=full_name
                )
                if response.is_existing
                else Messages.format(Messages.WELCOME_TEXT, full_name=full_name)
            )
            await message.answer(text, keyboard=kb_main())

        except Exception as e:
            logger.exception("VK RegisterUserController error: %s", e)
            await message.answer(Messages.ERROR_GENERIC, keyboard=kb_main())