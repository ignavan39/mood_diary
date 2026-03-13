from dataclasses import dataclass
from typing import Optional
from application.dtos import MoodStatsDTO
from domain.entities import StatsPeriod
from domain.entities.user import Platform
from domain.repositories import DiaryRepository, UserRepository


@dataclass
class GetUserStatsRequest:
    external_user_id: str
    platform: Platform
    period: StatsPeriod = StatsPeriod.WEEK


@dataclass
class GetUsetStatsResponse:
    success: bool
    stats: Optional[MoodStatsDTO] = None


class GetUserStatsUseCase:
    def __init__(self, diary_repo: DiaryRepository, user_repo: UserRepository):
        self._diary_repo = diary_repo
        self._user_repo = user_repo

    async def execute(self, request: GetUserStatsRequest) -> GetUsetStatsResponse:
        user = await self._user_repo.get_by_external_id(
            external_id=request.external_user_id,
            platfrom=request.platform,
        )
        if user is None or user.id is None:
            return GetUsetStatsResponse(success=False)

        stats_dict = await self._diary_repo.get_stats_by_user(
            user_id=user.id,
            period=request.period,
        )

        if not stats_dict or stats_dict.get("total_entries", 0) == 0:
            return GetUsetStatsResponse(
                stats=MoodStatsDTO(
                    total_entries=0,
                    avg_mood=0.0,
                    min_mood=0,
                    max_mood=0,
                    period_days=request.period.value,
                ),
                success=True,
            )

        return GetUsetStatsResponse(
            stats=MoodStatsDTO(
                total_entries=stats_dict.get("total_entries", 0),
                avg_mood=round(stats_dict.get("avg_mood", 0.0), 1),
                min_mood=stats_dict.get("min_mood", 0),
                max_mood=stats_dict.get("max_mood", 0),
                period_days=request.period.value,
                last_entry_date=stats_dict.get("last_entry_date"),
                first_entry_date=stats_dict.get("first_entry_date"),
            ),
            success=True,
        )
