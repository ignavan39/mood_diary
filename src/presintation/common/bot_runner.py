import asyncio
import logging
from typing import List

from presintation.common.base_bot import BaseBot

logger = logging.getLogger(__name__)

_MAX_RESTARTS = 5
_RESTART_DELAY = 5.0
_RESTART_RESET = 60.0


class BotRunner:
    def __init__(self, bots: List[BaseBot]) -> None:
        self._bots = bots
        self._tasks: List[asyncio.Task] = []

    async def start_all(self) -> None:
        if not self._bots:
            logger.warning("No bots to start")
            return

        logger.info("🚀 Starting %d bot(s)...", len(self._bots))

        self._tasks = [
            asyncio.create_task(
                self._run_bot_with_restart(bot),
                name=f"bot-{bot.get_platform_name()}",
            )
            for bot in self._bots
        ]

        results = await asyncio.gather(*self._tasks, return_exceptions=True)

        for bot, result in zip(self._bots, results):
            if isinstance(result, Exception):
                logger.error(
                    "%s bot exited with error: %s",
                    bot.get_platform_name(),
                    result,
                )

    async def stop_all(self) -> None:
        logger.info("Stopping %d bot(s)...", len(self._bots))

        for task in self._tasks:
            if not task.done():
                task.cancel()

        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

        for bot in self._bots:
            try:
                await bot.stop()
            except Exception as e:
                logger.error("Error stopping %s: %s", bot.get_platform_name(), e)

        logger.info("All bots stopped")

    async def _run_bot_with_restart(self, bot: BaseBot) -> None:
        platform = bot.get_platform_name()
        restarts = 0

        while True:
            start_time = asyncio.get_event_loop().time()
            try:
                logger.info("%s bot is running... (attempt %d)", platform, restarts + 1)
                await bot.start()
                logger.info("%s bot finished normally", platform)
                return

            except asyncio.CancelledError:
                logger.info("%s bot cancelled", platform)
                raise

            except Exception as e:
                uptime = asyncio.get_event_loop().time() - start_time

                if uptime >= _RESTART_RESET:
                    logger.info(
                        "%s bot ran for %.1fs — resetting restart counter",
                        platform,
                        uptime,
                    )
                    restarts = 0

                restarts += 1
                logger.exception(
                    "%s bot crashed (uptime %.1fs): %s", platform, uptime, e
                )

                if restarts >= _MAX_RESTARTS:
                    logger.error(
                        "%s bot exceeded max restarts (%d), giving up",
                        platform,
                        _MAX_RESTARTS,
                    )
                    raise

                delay = _RESTART_DELAY * restarts
                logger.info(
                    "Restarting %s bot in %.1fs... (%d/%d)",
                    platform,
                    delay,
                    restarts,
                    _MAX_RESTARTS,
                )
                await asyncio.sleep(delay)
