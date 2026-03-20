import asyncio
import logging
import signal
from typing import Optional, Callable, Coroutine, List

logger = logging.getLogger(__name__)


class SignalHandler:
    def __init__(self) -> None:
        self._shutdown_event = asyncio.Event()
        self._is_shutting_down = False
        self._shutdown_callbacks: List[Callable[[], Coroutine]] = []

    def register_callback(self, callback: Callable[[], Coroutine]) -> None:
        self._shutdown_callbacks.append(callback)

    async def shutdown(self, reason: str = "Shutdown requested") -> None:
        if self._is_shutting_down:
            logger.warning("Shutdown already in progress")
            return

        self._is_shutting_down = True
        logger.info("Shutdown initiated: %s", reason)

        for callback in self._shutdown_callbacks:
            try:
                await callback()
            except Exception as e:
                logger.error("Error in shutdown callback: %s", e)

        self._shutdown_event.set()
        logger.info("Shutdown completed")

    async def wait_for_shutdown(self, timeout: Optional[float] = None) -> bool:
        try:
            await asyncio.wait_for(self._shutdown_event.wait(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False

    def install_handlers(self) -> None:
        loop = asyncio.get_running_loop()

        loop.add_signal_handler(
            signal.SIGINT, lambda: asyncio.create_task(self.shutdown("SIGINT received"))
        )

        loop.add_signal_handler(
            signal.SIGTERM,
            lambda: asyncio.create_task(self.shutdown("SIGTERM received")),
        )

        logger.info("Signal handlers installed (SIGINT, SIGTERM)")

    @property
    def is_shutting_down(self) -> bool:
        return self._is_shutting_down


signal_handler = SignalHandler()
