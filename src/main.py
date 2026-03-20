# main.py
import asyncio
import logging
import sys
from typing import List

from sqlalchemy import text

from infrastructure import AppContainer
from infrastructure.concurrency import executor_pool
from infrastructure.configs import settings
from infrastructure.lifecycle import signal_handler
from infrastructure.metrics import (
    start_health_server_thread,
    start_metrics_server_thread,
)
from presintation.common import BotRunner
from presintation.common.base_bot import BaseBot
from presintation.telegram.bot import create_telegram_bot


logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)
container = AppContainer()


async def on_startup() -> None:
    await container.infrastructure.container.redis_cache().get_connection()
    session_manager = container.infrastructure.container.session_manager()
    async with session_manager.get_session() as session:
        await session.execute(text("SELECT 1"))
    logger.info("All connections warmed up")


async def on_shutdown() -> None:
    logger.info("Cleaning up...")
    await executor_pool.shutdown_all()
    await container.infrastructure.redis_cache().close()
    await container.infrastructure.session_manager().close()
    logger.info("Cleanup completed")


async def async_main() -> None:
    logger.info("Initializing infrastructure...")
    await on_startup()
    logger.info("Infrastructure initialized")

    bots: List[BaseBot] = []

    tg_bot = create_telegram_bot(container)
    if tg_bot is not None:
        bots.append(tg_bot)

    # vk_bot = create_vk_bot(container)
    # if vk_bot is not None:
    #     bots.append(vk_bot)

    if not bots:
        logger.error(
            "No bots enabled — set TG_BOT_ENABLED=true or VK_BOT_ENABLED=true in .env"
        )
        sys.exit(1)

    logger.info(
        "Created %d bot(s): %s",
        len(bots),
        ", ".join(b.get_platform_name() for b in bots),
    )

    start_health_server_thread(port=8080)
    start_metrics_server_thread(port=8000)

    logger.info("Health: http://localhost:8080/health")
    logger.info("Metrics: http://localhost:8000/metrics")

    runner = BotRunner(bots)
    start_task = asyncio.create_task(runner.start_all())

    try:
        shutdown_received = await signal_handler.wait_for_shutdown()
        if shutdown_received:
            logger.info("Shutdown signal received")
            await runner.stop_all()

        if not start_task.done():
            await start_task

    except asyncio.CancelledError:
        logger.info("Task cancelled")
        await runner.stop_all()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt")
        await signal_handler.shutdown("KeyboardInterrupt")
        await runner.stop_all()
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        await signal_handler.shutdown(f"Error: {e}")
        await runner.stop_all()
        sys.exit(1)
    finally:
        if not signal_handler.is_shutting_down:
            await signal_handler.shutdown("Final cleanup")


if __name__ == "__main__":
    try:
        logger.info("Mood Diary Bot starting...")
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Goodbye!")
    except Exception as e:
        logger.exception("Fatal error %s", e)
        sys.exit(1)