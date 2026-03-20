import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from presintation.common import Messages


logger = logging.getLogger(__name__)

PLATFORM = "telegram"


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(
                "Unhandled exception in Telegram handler [%s]: %s",
                type(event).__name__,
                e,
            )
            await self._reply_error(event)

    @staticmethod
    async def _reply_error(event: TelegramObject) -> None:
        try:
            if isinstance(event, Message):
                await event.answer(Messages.ERROR_GENERIC)
            elif isinstance(event, CallbackQuery):
                await event.answer(Messages.ERROR_GENERIC, show_alert=True)
        except Exception:
            pass
