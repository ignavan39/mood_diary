from aiogram import BaseMiddleware
from typing import Any

from infrastructure.database import DatabaseSessionManager


class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_manager: DatabaseSessionManager):
        self.session_manager = session_manager

    async def __call__(
        self,
        handler,
        event,
        data,
    ) -> Any:
        async with self.session_manager.get_session() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            except Exception:
                raise
