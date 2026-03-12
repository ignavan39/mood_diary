from datetime import date

from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from aiogram.fsm.context import FSMContext
from application.use_cases import GetUserStatsUseCase
from application.use_cases.get_user_stats import GetUserStatsRequest
from domain.entities import StatsPeriod
from presintation.telegram.endpoints.user.keyboards import (
    create_mood_stats_period_keyboard,
    create_mood_stats_with_refresh_keyboard,
)
from presintation.telegram.endpoints.user.states import StatsFlow


class ProfileController:
    def __init__(self, use_case: GetUserStatsUseCase) -> None:
        self.use_case = use_case

    async def call(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        if message.from_user is None:
            return

        user_id = message.from_user.id

        await self._send_stats_message(message, user_id, StatsPeriod.WEEK)

        await state.set_state(StatsFlow.viewing_stats)

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

            await self._send_stats_message(callback.message, user_id, period)
            await callback.answer()
        except ValueError:
            await callback.answer("❌ Неверный период", show_alert=True)
        except Exception:
            await callback.answer("⚠️ Ошибка. Попробуйте позже.", show_alert=True)

    async def _send_stats_message(
        self,
        message: Message | InaccessibleMessage,
        user_id: int,
        period: StatsPeriod,
    ) -> None:

        request = GetUserStatsRequest(external_user_id=user_id, period=period)
        response = await self.use_case.execute(request)
        stats = response.stats

        if not response.success:
            await message.answer(
                "⚠️ Ошибка при получении статистики. Попробуйте позже.",
                reply_markup=create_mood_stats_period_keyboard().as_markup(),
            )
            return

        if stats is None or stats.total_entries == 0:
            await message.answer(
                f"📊 Статистика: {period.label}\n\n"
                f"❌ Нет записей за этот период.\n\n"
                f"Используй /mood чтобы добавить первую запись!",
                reply_markup=create_mood_stats_period_keyboard().as_markup(),
            )
            return

        last_entry = "—"
        if stats.last_entry_date:
            if isinstance(stats.last_entry_date, date):
                last_entry = stats.last_entry_date.strftime("%d.%m.%Y")
            else:
                last_entry = str(stats.last_entry_date)[:10]

        first_entry = "—"
        if stats.first_entry_date:
            if isinstance(stats.first_entry_date, date):
                first_entry = stats.first_entry_date.strftime("%d.%m.%Y")
            else:
                first_entry = str(stats.first_entry_date)[:10]

        text = (
            f"📊 Статистика: {period.label}\n\n"
            f"{stats.mood_emoji} Среднее настроение: {stats.avg_mood}/10 ({stats.mood_text})\n\n"
            f"📈 Детали:\n"
            f"• Записей: {stats.total_entries}\n"
            f"• Минимум: {stats.min_mood}/10\n"
            f"• Максимум: {stats.max_mood}/10\n\n"
            f"🕐 Период:\n"
            f"• Первая запись: {first_entry}\n"
            f"• Последняя: {last_entry}\n\n"
            f"Выберите другой период:"
        )

        await message.answer(
            text,
            reply_markup=create_mood_stats_with_refresh_keyboard(period).as_markup(),
        )
