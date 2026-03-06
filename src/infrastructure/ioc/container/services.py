from dependency_injector import containers, providers

from application.use_cases import RegisterUserUseCase
from infrastructure.ioc.container.infrastructure import InfrastructureContainer


class ServicesContainer(containers.DeclarativeContainer):
    infrastructure: providers.Container[InfrastructureContainer] = providers.Container(
        InfrastructureContainer
    )

    register_user_use_case: providers.Factory[RegisterUserUseCase] = providers.Factory(
        RegisterUserUseCase, user_repo=infrastructure.user_repository.provided
    )
