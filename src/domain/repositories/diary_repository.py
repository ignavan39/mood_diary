from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

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
    async def get_many_by_user_and_timerange(self, filters: DiaryFilter) -> List[Diary]:
        """
        Get diary entries with filter.

        Args:
            filter: Filter criteria

        Returns:
            List of Diary entries
        """
        pass
