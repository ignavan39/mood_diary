from abc import ABC, abstractmethod
from typing import Any, Optional


class Cache(ABC):
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool: ...

    @abstractmethod
    async def get(self, key: str) -> Optional[dict] | None: ...

    @abstractmethod
    async def delete(self, key: str) -> int: ...

    @abstractmethod
    async def delete_by_pattern(self, pattern: str) -> None: ...

    @abstractmethod
    async def exists(self, key: str) -> bool: ...
