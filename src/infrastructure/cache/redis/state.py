import logging
from enum import Enum, auto
from typing import Optional, Dict, Any

from infrastructure.cache.redis import RedisManager


logger = logging.getLogger(__name__)


class UserState(Enum):
    NONE = auto()
    SELECTING_MOOD = auto()
    CONFIRMING_UPDATE = auto()
    VIEWING_STATS = auto()


class UniversalStateManager:
    KEY_PREFIX = "mood_diary:state"
    DATA_PREFIX = "mood_diary:state_data"
    DEFAULT_TTL = 3600

    def __init__(self, redis_manager: RedisManager) -> None:
        self._redis = redis_manager

    def _state_key(self, platform: str, user_id: int) -> str:
        return f"{self.KEY_PREFIX}:{platform}:{user_id}"

    def _data_key(self, platform: str, user_id: int) -> str:
        return f"{self.DATA_PREFIX}:{platform}:{user_id}"

    async def set_state(
        self,
        platform: str,
        user_id: int,
        state: UserState,
        ttl: Optional[int] = None,
    ) -> bool:
        key = self._state_key(platform, user_id)
        return await self._redis.set(key, state.name, ttl=ttl or self.DEFAULT_TTL)

    async def get_state(self, platform: str, user_id: int) -> Optional[UserState]:
        key = self._state_key(platform, user_id)
        value = await self._redis.get(key)

        if value and value in UserState.__members__:
            return UserState[value]
        return None

    async def clear_state(self, platform: str, user_id: int) -> int:
        keys = [
            self._state_key(platform, user_id),
            self._data_key(platform, user_id),
        ]
        return await self._redis.delete(*keys)

    async def set_data(
        self,
        platform: str,
        user_id: int,
        data: Dict[str, Any],
        ttl: Optional[int] = None,
    ) -> bool:
        key = self._data_key(platform, user_id)
        return await self._redis.set_json(key, data, ttl=ttl or self.DEFAULT_TTL)

    async def get_data(self, platform: str, user_id: int) -> Optional[Dict[str, Any]]:
        key = self._data_key(platform, user_id)
        return await self._redis.get_json(key)

    async def update_data(
        self,
        platform: str,
        user_id: int,
        updates: Dict[str, Any],
    ) -> bool:
        existing = await self.get_data(platform, user_id) or {}
        existing.update(updates)
        return await self.set_data(platform, user_id, existing)

    async def reset(self, platform: str, user_id: int) -> None:
        await self.clear_state(platform, user_id)
        logger.debug("Reset state for %s:%d", platform, user_id)
