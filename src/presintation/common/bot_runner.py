import asyncio
import logging
from typing import List

from presintation.common.base_bot import BaseBot


logger = logging.getLogger(__name__)


class BotRunner:
    def __init__(self, bots: List[BaseBot]):
        self._bots = bots
        self._tasks: List[asyncio.Task] = []
    
    async def start_all(self) -> None:
        if not self._bots:
            logger.warning("No bots to start")
            return
        
        logger.info("🚀 Starting %d bot(s)...", len(self._bots))
        
        self._tasks = [
            asyncio.create_task(self._run_bot(bot))
            for bot in self._bots
        ]
        
        try:
            await asyncio.gather(*self._tasks)
        except asyncio.CancelledError:
            logger.info("Bot tasks cancelled")
        except Exception as e:
            logger.exception("Bot runner error: %s", e)
            raise
    
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
    
    async def _run_bot(self, bot: BaseBot) -> None:

        platform = bot.get_platform_name()
        
        try:
            logger.info("🤖 %s Bot is running...", platform)
            await bot.start()
        except asyncio.CancelledError:
            logger.info("%s Bot cancelled", platform)
            raise
        except Exception as e:
            logger.exception("%s Bot crashed: %s", platform, e)
            raise
        finally:
            logger.info("🏁 %s Bot finished", platform)