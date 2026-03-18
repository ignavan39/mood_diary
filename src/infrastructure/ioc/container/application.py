from dependency_injector import containers, providers

from infrastructure.ioc.container.infrastructure import InfrastructureContainer
from infrastructure.ioc.container.services import (
    ServicesContainer,
)


class AppContainer(containers.DeclarativeContainer):
    infrastructure: providers.Container[InfrastructureContainer] = providers.Container(
        InfrastructureContainer
    )

    services: providers.Container[ServicesContainer] = providers.Container(
        ServicesContainer,
        infrastructure=infrastructure,
    )
