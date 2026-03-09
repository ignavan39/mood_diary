from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional

from application.dtos import StatsPeriod
from domain.entities import Diary


@dataclass
class DiaryFilter:
    user_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0


class DiaryRepository(ABC):
    @abstractmethod
    async def save(self, diary: Diary) -> Optional[Diary]:
        """Persist a diary and return it with generated ID"""
        pass

    @abstractmethod
    async def get_stats_by_user_and_timerange(
        self, filters: DiaryFilter
    ) -> Optional[dict]:
        """
        Get mood statistics for a user.
        Returns aggregate data calculated in DB (faster than Python).
        """
        pass

    @abstractmethod
    async def get_stats_by_user(
        self,
        user_id: int,
        period: StatsPeriod,
    ) -> Optional[dict]:
        """
        Get mood statistics for a user over a period.
        Returns aggregate data calculated in DB.
        """
        pass
