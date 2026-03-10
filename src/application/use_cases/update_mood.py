from dataclasses import dataclass

from domain.repositories.diary_repository import DiaryRepository


@dataclass
class UpdateMoodRequest:
    diary_id: int
    new_rating: int


@dataclass
class UpdateMoodResponse:
    success: bool
    diary_id: int
    old_rating: int
    new_rating: int


class UpdateMoodUseCase:
    def __init__(self, diary_repo: DiaryRepository):
        self._diary_repo = diary_repo

    # async def execute(self, request: UpdateMoodRequest) -> UpdateMoodResponse:
