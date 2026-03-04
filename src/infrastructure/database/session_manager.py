import contextlib
import logging
import threading
from typing import Any, AsyncIterator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.configs import settings

logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    _instance: Optional["DatabaseSessionManager"] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}) -> None:
        if not hasattr(self, "_initialized"):
            with self._lock:
                if not hasattr(self, "_initialized"):
                    self._engine = create_async_engine(host, **engine_kwargs)
                    self._session_factory = async_sessionmaker(
                        autocommit=False,
                        bind=self._engine,
                        expire_on_commit=False,
                        autoflush=False,
                    )
                    self._initialized = True

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
