from abc import ABC, abstractmethod

class Notify(ABC):

    @property
    @abstractmethod
    def get_name(self) -> str: ...

    @abstractmethod
    async def register(self) -> None: ...

    @abstractmethod
    async def notify(self) -> None: ...
