import logging
from typing import TYPE_CHECKING, ClassVar

from application.use_cases.get_user_stats import (
    GetUserStatsRequest,
    GetUserStatsUseCase,
)
from domain.entities.stats_period import StatsPeriod
from domain.exceptions import UserNotFoundError
from presentation.common.messages import Messages
from presentation.vk.handlers.base import VkHandler
from presentation.vk.keyboards import kb_stats_period
from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.types import VkMessage

if TYPE_CHECKING:
    from infrastructure import AppContainer
    from vk_api import VkApi

logger = logging.getLogger(__name__)
PLATFORM = "vk"


class GetPofileMenuHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = (
        Messages.BTN_STATS,
        Messages.BTN_PROFILE,
        "/profile",
        "статистика",
        "profile",
    )

    async def handle(self, message: VkMessage) -> bool:
        if not self._matches_command(message.text.lower()):
            return False

        await self._send_message(
            user_id=message.from_user.id,
            text=Messages.CHOOSE_PERIOD,
            keyboard=kb_stats_period(),
        )
        return True


class GetProfileHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = ()

    def __init__(
        self,
        vk_api: "VkApi",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        super().__init__(vk_api, container, group_id)
        self._use_case: GetUserStatsUseCase = (
            container.services.get_user_stats_use_case()
        )

    def _matches_period(self, message: VkMessage) -> bool:
        if message.payload and "period" in message.payload:
            return True

        period = Messages.get_period_label_by_str(message.text.strip())
        return period is not None

    async def handle(self, message: VkMessage) -> bool:
        if not self._matches_period(message):
            return False

        logger.info(
            "VK period selected by user %d: '%s'", message.from_user.id, message.text
        )

        try:
            if message.payload and "period" in message.payload:
                period = StatsPeriod(int(message.payload["period"]))
            else:
                period = Messages.get_period_label_by_str(message.text.strip())
                if period is None:
                    logger.warning("Unknown period label: %s", message.text)
                    return False

            response = await self._use_case.execute(
                GetUserStatsRequest(
                    external_user_id=str(message.from_user.id),
                    platform=PLATFORM,
                    period=period,
                )
            )

            if (
                not response.success
                or response.stats is None
                or response.stats.total_entries == 0
            ):
                await self._send_message(
                    user_id=message.from_user.id,
                    text=Messages.STATS_NO_DATA,
                    keyboard=kb_main(),
                )
                return True

            s = response.stats
            period_label = Messages.get_period_str_by_day(period.value)

            text = (
                Messages.format(Messages.STATS_TITLE, period=period_label)
                + "\n\n"
                + Messages.format(
                    Messages.STATS_DETAILS,
                    emoji=Messages.get_mood_emoji(int(s.avg_mood)),
                    avg=s.avg_mood,
                    mood_text=Messages.get_mood_text(s.avg_mood),
                    total=s.total_entries,
                    min=s.min_mood,
                    max=s.max_mood,
                    first=s.first_entry_date or "—",
                    last=s.last_entry_date or "—",
                )
            )

            await self._send_message(
                user_id=message.from_user.id,
                text=text,
                keyboard=kb_main(),
            )

            return True

        except UserNotFoundError:
            await self._send_message(
                user_id=message.from_user.id,
                text=Messages.STATS_NO_DATA,
                keyboard=kb_main(),
            )
            return True

        except Exception as e:
            logger.exception("GetProfileHandler error: %s", e)
            await self._send_message(
                user_id=message.from_user.id,
                text=Messages.ERROR_GENERIC,
                keyboard=kb_main(),
            )
            return True
