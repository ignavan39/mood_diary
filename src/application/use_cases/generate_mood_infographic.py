import logging
from datetime import datetime, timedelta, date
from typing import List

from application.dtos import Trend
from domain.entities import Diary
from domain.exceptions import UserNotFoundError
from domain.repositories import UserRepository
from domain.repositories.diary_repository import DiaryFilter, DiaryRepository
from application.services.chart_generator import ChartGeneratorInterface, ChartData
from application.dtos.infographic_dtos import (
    GenerateInfographicRequest,
    GenerateInfographicResponse,
    InfographicStats,
)

logger = logging.getLogger(__name__)


class GenerateMoodInfographicUseCase:
    def __init__(
        self,
        diary_repo: DiaryRepository,
        user_repo: UserRepository,
        chart_generator: ChartGeneratorInterface,
    ):
        self._diary_repo = diary_repo
        self._user_repo = user_repo
        self._chart_generator = chart_generator

    async def execute(
        self, request: GenerateInfographicRequest
    ) -> GenerateInfographicResponse:
        logger.info(
            "Generating infographic for user %s (period: %d days)",
            request.external_user_id,
            request.days,
        )

        user = await self._user_repo.get_by_external_id(
            external_id=str(request.external_user_id), platfrom=request.platform
        )
        if user is None:
            raise UserNotFoundError(external_user_id=str(request.external_user_id))

        diaries = await self._get_diaries_for_period(user.id, request.days)

        if not diaries:
            image_buffer = await self._chart_generator.generate_empty(
                period_days=request.days,
                theme=request.theme,
            )
            image_buffer.seek(0)

            return GenerateInfographicResponse(
                image_data=image_buffer,
                filename=f"mood_diary_{request.external_user_id}_{date.today()}_nodata.{request.format}",
                stats=InfographicStats(
                    total_entries=0,
                    avg_mood=0,
                    min_mood=0,
                    max_mood=0,
                    trend="stable",
                    period_days=request.days,
                ),
                is_empty=True,
            )

        chart_data, stats = self._prepare_chart_data_and_stats(diaries, request.days)

        image_buffer = await self._chart_generator.generate(
            data=chart_data,
            chart_type=request.chart_type,
            theme=request.theme,
            include_stats=request.include_stats,
            user_id=user.id,
        )

        image_buffer.seek(0)
        logger.info(
            "Infographic generated: %s (%d bytes)",
            stats.period_days,
            len(image_buffer.getvalue()),
        )

        return GenerateInfographicResponse(
            image_data=image_buffer,
            filename=f"mood_diary_{request.external_user_id}_{date.today()}.{request.format}",
            stats=stats,
            is_empty=False,
        )

    async def _get_diaries_for_period(self, user_id: int, days: int) -> List[Diary]:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        return await self._diary_repo.get_many_by_user_and_timerange(
            filters=DiaryFilter(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                limit=1000,
            )
        )

    def _prepare_chart_data_and_stats(
        self, diaries: List[Diary], days: int
    ) -> tuple[ChartData, InfographicStats]:
        values = [d.rating for d in diaries]
        dates = [d.date for d in diaries]

        total = len(values)
        avg = sum(values) / total
        min_mood = min(values)
        max_mood = max(values)
        trend = self._calculate_trend(values)

        chart_data: ChartData = ChartData(
            dates=dates,
            values=values,
            stats={
                "total_entries": total,
                "avg_mood": avg,
                "min_mood": min_mood,
                "max_mood": max_mood,
                "trend": trend,
            },
            period_days=days,
        )

        stats = InfographicStats(
            total_entries=total,
            avg_mood=avg,
            min_mood=min_mood,
            max_mood=max_mood,
            trend=trend,
            period_days=days,
            first_entry_date=dates[0] if dates else None,
            last_entry_date=dates[-1] if dates else None,
        )

        return chart_data, stats

    def _calculate_trend(self, values: List[int]) -> Trend:
        if len(values) < 2:
            return "stable"
        mid = len(values) // 2
        first_half_avg = sum(values[:mid]) / mid
        second_half_avg = sum(values[mid:]) / (len(values) - mid)
        diff = second_half_avg - first_half_avg
        if diff > 1:
            return "improving"
        elif diff < -1:
            return "declining"
        else:
            return "stable"
