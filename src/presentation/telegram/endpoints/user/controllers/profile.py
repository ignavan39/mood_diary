from math import ceil

from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from application.use_cases import GetUserStatsUseCase
from application.use_cases.get_user_stats import GetUserStatsRequest
from domain.entities import StatsPeriod
from presentation.common import Messages
from presentation.telegram.endpoints.user.keyboards import (
    create_mood_stats_period_keyboard,
    create_mood_stats_with_refresh_keyboard,
)


class ProfileController:
    def __init__(self, use_case: GetUserStatsUseCase) -> None:
        self.use_case = use_case

    async def call(
        self,
        message: Message,
    ) -> None:
        if message.from_user is None:
            return

        user_id = message.from_user.id

        await self._send_stats_message(message, str(user_id), StatsPeriod.WEEK)

    async def handle_stats_period(
        self,
        callback: CallbackQuery,
    ) -> None:
        if (
            callback.from_user is None
            or callback.message is None
            or callback.data is None
        ):
            return

        try:
            days = int(callback.data.split("_")[1])
            period = StatsPeriod(days)
            user_id = callback.from_user.id

            await self._send_stats_message(callback.message, str(user_id), period)
            await callback.answer()
        except ValueError:
            await callback.answer(Messages.INVALID_PERIOD, show_alert=True)
        except Exception:
            await callback.answer(Messages.ERROR_GENERIC, show_alert=True)

    async def _send_stats_message(
        self,
        message: Message | InaccessibleMessage,
        user_id: str,
        period: StatsPeriod,
    ) -> None:

        request = GetUserStatsRequest(
            external_user_id=user_id, period=period, platform="telegram"
        )
        response = await self.use_case.execute(request)
        stats = response.stats

        if not response.success:
            await message.answer(
                Messages.ERROR_GENERIC,
                reply_markup=create_mood_stats_period_keyboard().as_markup(),
            )
            return

        if stats is None or stats.total_entries == 0:
            error_text = Messages.format(Messages.STATS_NO_DATA, period=period.label)
            await message.answer(
                error_text,
                reply_markup=create_mood_stats_period_keyboard().as_markup(),
            )
            return

        emoji = Messages.get_mood_emoji(ceil(stats.avg_mood))
        mood_text = Messages.format(Messages.get_mood_text(stats.avg_mood))

        text = Messages.format(
            Messages.STATS_DETAILS,
            emoji=emoji,
            mood_text=mood_text,
            period=period.label,
            avg=stats.avg_mood,
            min=stats.min_mood,
            max=stats.max_mood,
            total=stats.total_entries,
            first=stats.first_entry_date,
            last=stats.last_entry_date,
        )

        await message.answer(
            text,
            reply_markup=create_mood_stats_with_refresh_keyboard(period).as_markup(),
        )
