from dependency_injector import containers, providers


from infrastructure.ioc.container.services import (
    InfrastructureContainer,
    ServicesContainer,
)


class AppContainer(containers.DeclarativeContainer):
    infrastructure = providers.Container(InfrastructureContainer)
    services = providers.Container(ServicesContainer)
