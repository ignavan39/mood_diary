import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

logger = logging.getLogger(__name__)


class ExecutorPool:
    _instance: Optional["ExecutorPool"] = None
    _executors: dict[str, ThreadPoolExecutor]
    
    def __new__(cls) -> "ExecutorPool":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._executors = {}
        return cls._instance
    
    def get_executor(self, name: str, max_workers: int = 4) -> ThreadPoolExecutor:
        if name not in self._executors:
            logger.info("Creating executor pool '%s' with %d workers", name, max_workers)
            self._executors[name] = ThreadPoolExecutor(max_workers=max_workers)
        
        return self._executors[name]
    
    async def shutdown_all(self) -> None:
        for name, executor in self._executors.items():
            logger.info("🛑 Shutting down executor pool '%s'", name)
            executor.shutdown(wait=True)
        
        self._executors.clear()
        logger.info("All executor pools shutdown")
    
    def get_stats(self) -> dict:
        return {
            name: {
                "max_workers": executor._max_workers,
            }
            for name, executor in self._executors.items()
        }


executor_pool = ExecutorPool()