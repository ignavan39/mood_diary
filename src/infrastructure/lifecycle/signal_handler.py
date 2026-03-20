import asyncio
import logging
import signal
from typing import Callable, Coroutine, List, Optional

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
            return

        self._is_shutting_down = True
        logger.info("Shutdown initiated: %s", reason)

        if self._shutdown_callbacks:
            results = await asyncio.gather(
                *[cb() for cb in self._shutdown_callbacks],
                return_exceptions=True,
            )
            for cb, result in zip(self._shutdown_callbacks, results):
                if isinstance(result, Exception):
                    logger.error(
                        "Error in shutdown callback %s: %s",
                        getattr(cb, "__name__", cb),
                        result,
                    )

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

        for sig, reason in (
            (signal.SIGINT, "SIGINT received"),
            (signal.SIGTERM, "SIGTERM received"),
        ):
            def func(r=reason) -> asyncio.Task[None]:
                return asyncio.create_task(self.shutdown(r))
            loop.add_signal_handler(
                sig,
                func,
            )

        logger.info("Signal handlers installed (SIGINT, SIGTERM)")

    @property
    def is_shutting_down(self) -> bool:
        return self._is_shutting_down


signal_handler = SignalHandler()