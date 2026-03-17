from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import List, Literal, Optional

from domain.dtos import SaveDiaryDTO, UpdateDiaryDTO
from domain.entities import Diary, StatsPeriod

OrderBy = Literal["date_asc", "date_desc", "rating_asc", "rating_desc"]

@dataclass
class DiaryFilter:
    user_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0
    order_by: OrderBy = "date_asc"


class DiaryRepository(ABC):
    @abstractmethod
    async def save(self, diary: SaveDiaryDTO) -> Optional[Diary]:
        """Persist a diary and return it with generated ID"""
        pass

    @abstractmethod
    async def get_stats_by_user_and_timerange(
        self, filters: DiaryFilter
    ) -> Optional[dict]:
        pass

    @abstractmethod
    async def update(self, diary: UpdateDiaryDTO) -> Diary:
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

    @abstractmethod
    async def get_by_id(self, diary_id: int) -> Optional[Diary]:
        pass

    @abstractmethod
    async def get_by_user_and_date(self, user_id: int, date: date) -> Optional[Diary]:
        pass

    @abstractmethod
    async def get_many_by_user_and_timerange(self, filters: DiaryFilter) -> List[Diary]:
        pass
