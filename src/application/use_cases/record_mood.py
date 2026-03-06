from dataclasses import dataclass
from datetime import date
from domain.repositories import DiaryRepository


@dataclass
class RecordMoodRequest:
    user_id: int
    rating: int
    date: date


@dataclass
class RecordMoodResponse:
    success: bool
    is_existing: bool = False


class RecordMoodUseCase:
    def __init__(self, diary_repo: DiaryRepository):
        self._diary_repo = diary_repo
