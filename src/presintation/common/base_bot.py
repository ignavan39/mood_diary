from abc import ABC, abstractmethod

from infrastructure import AppContainer


class BaseBot(ABC):
    def __init__(self, container: "AppContainer"):
        self._container = container

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass

    @staticmethod
    def get_platform_name() -> str:
        return "Unknown"
