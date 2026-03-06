from dataclasses import dataclass
from datetime import datetime, timedelta
import math
from typing import List
from domain.entities import Diary
from domain.repositories import DiaryRepository, UserRepository
from domain.repositories.diary_repository import DiaryFilter


@dataclass
class GetUserWeeklyStatsRequest:
    external_user_id: int


@dataclass
class Stats:
    total: int = 0
    avg_mood: int = 0
    min_mood: int = 0
    max_mood: int = 0


@dataclass
class GetUserWeeklyStatsResponse:
    stats: Stats | None = None
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

        diaries: List[Diary] = await self._diary_repo.get_many_by_user_and_timerange(
            filters=DiaryFilter(
                user_id=user.id, start_date=start_date.date(), end_date=end_date.date()
            )
        )

        if not diaries:
            return GetUserWeeklyStatsResponse(Stats(), success=True)

        moods = [d.rating for d in diaries]

        return GetUserWeeklyStatsResponse(
            Stats(
                total=len(moods),
                avg_mood=math.ceil(sum(moods) / len(moods)),
                min_mood=min(moods),
                max_mood=max(moods),
            ),
            success=True,
        )
