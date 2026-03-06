from dataclasses import dataclass
from datetime import datetime, timedelta
from application.dtos import MoodStatsDTO
from domain.repositories import DiaryRepository, UserRepository
from domain.repositories.diary_repository import DiaryFilter


@dataclass
class GetUserWeeklyStatsRequest:
    external_user_id: int
    stats: MoodStatsDTO


@dataclass
class GetUserWeeklyStatsResponse:
    stats: MoodStatsDTO | None = None
    success: bool = False


class GetUserWeeklyStatsUseCase:
    def __init__(self, diary_repo: DiaryRepository, user_repo: UserRepository):
        self._diary_repo = diary_repo
        self._user_repo = user_repo

    async def execute(
        self, external_user_id, days: int = 7
    ) -> GetUserWeeklyStatsResponse:
        user = await self._user_repo.get_by_external_id(external_id=external_user_id)
        if user is None or user.id is None:
            return GetUserWeeklyStatsResponse(success=False)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        stats = await self._diary_repo.get_stats_by_user_and_timerange(
            DiaryFilter(user_id=user.id, start_date=start_date, end_date=end_date)
        )

        if not stats or stats.get("total_entries", 0) == 0:
            return GetUserWeeklyStatsResponse(
                MoodStatsDTO(
                    total=0,
                    avg_mood=0,
                    min_mood=0,
                    max_mood=0,
                ),
                success=True,
            )

        return GetUserWeeklyStatsResponse(
            MoodStatsDTO(
                total=stats.get("total", 0),
                avg_mood=round(stats.get("avg_mood", 0.0), 1),
                min_mood=stats.get("min_mood", 0),
                max_mood=stats.get("max_mood", 0),
                period_days=days,
            ),
            success=True,
        )
