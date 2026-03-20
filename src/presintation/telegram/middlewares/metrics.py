import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from infrastructure.metrics.metrics import bot_messages_total, bot_request_duration
from presintation.common.messages import Messages


class MetricsMiddleware(BaseMiddleware):
    PLATFORM = "telegram"

    CALLBACK_PREFIX_MAP: dict[str, str] = {
        "mood_": "mood",
        "update_yes_": "update_mood",
        "update_no_": "update_mood",
        "stats_": "stats",
        "cmd_": "menu",
    }

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        command = self._resolve_command(event)
        start = time.perf_counter()
        status = "success"

        try:
            return await handler(event, data)
        except Exception:
            status = "error"
            raise
        finally:
            duration = time.perf_counter() - start
            bot_messages_total.labels(
                platform=self.PLATFORM,
                command=command,
                status=status,
            ).inc()
            bot_request_duration.labels(
                platform=self.PLATFORM,
                command=command,
            ).observe(duration)

    def _resolve_command(self, event: TelegramObject) -> str:
        if isinstance(event, Message):
            return self._command_from_message(event)
        if isinstance(event, CallbackQuery):
            return self._command_from_callback(event)
        return "unknown"

    def _command_from_message(self, message: Message) -> str:
        text = (message.text or "").strip()

        if text.startswith("/"):
            return text.split()[0][1:].lower()

        command = Messages.get_command_by_btn(text)
        if command:
            return command

        if text.isdigit() and 0 <= int(text) <= 10:
            return "mood_value"

        return "unknown"

    def _command_from_callback(self, callback: CallbackQuery) -> str:
        data = callback.data or ""

        for prefix, command in self.CALLBACK_PREFIX_MAP.items():
            if data.startswith(prefix):
                return command

        return "unknown"
