from dependency_injector import containers, providers
from dependency_injector.providers import Factory, Singleton

from domain.repositories import DiaryRepository, UserRepository
from infrastructure.cache.redis import RedisManager
from infrastructure.configs.config import Settings
from infrastructure.database import DatabaseSessionManager
from infrastructure.database.repositories.sqlachemy import (
    SQLAchemyDiaryRepository,
    SQLAchemyUserRepository,
)


class InfrastructureContainer(containers.DeclarativeContainer):
    # TODO: provider.Configuration()
    settingsFactory = providers.Singleton(Settings)
    settings = settingsFactory()

    session_manager: Singleton[DatabaseSessionManager] = providers.Singleton(
        DatabaseSessionManager, host=settings.db.url
    )

    redis_cache: Singleton[RedisManager] = providers.Singleton(
        RedisManager,
        host=settings.redis_cache.host,
        port=settings.redis_cache.port,
        password=settings.redis_cache.password,
        db=settings.redis_cache.db,
    )

    user_repository: Factory[UserRepository] = providers.Factory(
        SQLAchemyUserRepository,
        session_manager=session_manager.provided,
    )

    diary_repository: Factory[DiaryRepository] = providers.Factory(
        SQLAchemyDiaryRepository, session_manager=session_manager.provided
    )
