import contextlib
import logging
from typing import Any, AsyncIterator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from infrastructure.configs import settings

logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}) -> None:
        logger.info("Initializing DatabaseSessionManager...")
        self._engine = create_async_engine(
            host,
            **engine_kwargs,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        self._session_factory = async_sessionmaker(
            autocommit=False,
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
        )
        logger.info("DatabaseSessionManager initialized")

    async def close(self) -> None:
        await self._engine.dispose()

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        session_id = id(self)
        logger.debug("[%s] Creating new session", session_id)

        try:
            async with self._session_factory() as session:
                logger.debug("[%s] Session acquired", session_id)
                try:
                    yield session
                    await session.commit()
                except Exception as e:
                    logger.warning("[%s] Rolling back transaction: %s", session_id, e)
                    await session.rollback()
                    raise
                finally:
                    logger.debug("[%s] Closing session", session_id)
                    await session.close()
                    logger.debug("[%s] Session closed", session_id)
        except Exception as e:
            logger.error("[%s] Failed to create session: %s", session_id, e)
            raise


_default_session_manager: Optional[DatabaseSessionManager] = None


def get_session_manager() -> DatabaseSessionManager:
    global _default_session_manager
    if _default_session_manager is None:
        _default_session_manager = DatabaseSessionManager(settings.db.get_url())
    return _default_session_manager


def reset_default_session_manager() -> None:
    global _default_session_manager
    _default_session_manager = None
