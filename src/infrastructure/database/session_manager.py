import contextlib
import logging
from typing import Any, AsyncIterator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.configs import settings

logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    _instance: Optional["DatabaseSessionManager"] = None

    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}) -> None:
        self._engine = create_async_engine(host, **engine_kwargs)
        self._session_factory = async_sessionmaker(
            autocommit=False,
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
        )

    async def close(self) -> None:
        await self._engine.dispose()

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
            finally:
                await session.close()

database_session_manager = DatabaseSessionManager(settings.db.get_url())