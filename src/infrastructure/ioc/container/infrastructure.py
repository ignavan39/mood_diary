from dependency_injector import containers, providers
from dependency_injector.providers import Factory, Singleton

from domain.repositories import UserRepository
from infrastructure.configs.config import Settings
from infrastructure.database import DatabaseSessionManager
from infrastructure.database.repositories import SQLAchemyUserRepository


class InfrastructureContainer(containers.DeclarativeContainer):
    # TODO: provider.Configuration()
    settings = providers.Singleton(Settings)

    session_manager: Singleton[DatabaseSessionManager] = providers.Singleton(
        DatabaseSessionManager, host=settings().db.get_url()
    )

    user_repository: Factory[UserRepository] = providers.Factory(
        SQLAchemyUserRepository,
        session_manager=session_manager.provided,
    )
