from infrastructure.ioc.container.application import AppContainer


container = AppContainer()
container.wire(packages=[__name__])
