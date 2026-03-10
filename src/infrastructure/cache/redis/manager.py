import json
import logging
from typing import Any, Optional
from redis.asyncio import Redis as AsyncRedis, ConnectionPool

logger = logging.getLogger(__name__)


class RedisManager:    
    def __init__(
        self,
        host: str,
        port: int,
        password: str,
        db: int = 0,
        **kwargs: Any,
    ) -> None:
        self._host = host
        self._port = port
        self._password = password
        self._db = db
        self._kwargs = kwargs
        
        self._redis: Optional[AsyncRedis] = None
        self._pool: Optional[ConnectionPool] = None
        
        logger.info("RedisManager initialized (config: %s:%d)", host, port)
    
    async def _connect(self) -> AsyncRedis:
      logger.info("Establishing Redis connection...")
      
      self._pool = ConnectionPool(
          host=self._host,
          port=self._port,
          password=self._password,
          db=self._db,
          decode_responses=True,
          max_connections=50,
          health_check_interval=30,
          socket_connect_timeout=5,
          socket_timeout=5,
          **self._kwargs,
      )
      
      redis = AsyncRedis(connection_pool=self._pool)
      
      try:
          await redis.ping() # type: ignore
          logger.info("Redis connected successfully")
      except Exception as e:
        self._redis = None
        if self._pool:
            await self._pool.disconnect()
            self._pool = None
        logger.error("Failed to connect to Redis: %s", e)
        raise
      return redis

    async def get_connection(self) -> AsyncRedis:
        if self._redis is None:
          self._redis = await self._connect()
        
        return self._redis
    
    async def close(self) -> None:
        if self._pool:
            await self._pool.disconnect()
            self._pool = None
            self._redis = None
            logger.info("Redis connection closed")

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        redis = await self.get_connection()
        return await redis.set(key, str(value), ex=ttl)
    
    async def get(self, key: str) -> Optional[str]:
        redis = await self.get_connection()
        return await redis.get(key)
    
    async def delete(self, key: str) -> int:
        redis = await self.get_connection()
        return await redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        redis = await self.get_connection()
        return await redis.exists(key) == 1
    
    async def get_json(self, key: str) -> Optional[dict]:
        redis = await self.get_connection()
        value = await redis.get(key)
        return json.loads(value) if value else None
    
    async def set_json(self, key: str, value: dict, ttl: Optional[int] = None) -> bool:
        redis = await self.get_connection()
        return await redis.set(key, json.dumps(value), ex=ttl)
    