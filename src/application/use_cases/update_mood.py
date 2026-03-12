from dataclasses import dataclass
from datetime import date as date_type
from domain.dtos import UpdateDiaryDTO
from domain.exceptions import InvalidDiaryRatingError
from domain.exceptions.exceptions import DiaryNotFoundError
from domain.repositories.diary_repository import DiaryRepository


@dataclass
class UpdateMoodRequest:
    diary_id: int
    new_rating: int
    date: date_type


@dataclass
class UpdateMoodResponse:
    success: bool
    diary_id: int
    old_rating: int
    new_rating: int


class UpdateMoodUseCase:
    def __init__(self, diary_repo: DiaryRepository):
        self._diary_repo = diary_repo

    async def execute(self, req: UpdateMoodRequest) -> UpdateMoodResponse:
        if req.new_rating < 0 or req.new_rating > 10:
            raise InvalidDiaryRatingError(rating=req.new_rating)
        existing = await self._diary_repo.get_by_id(req.diary_id)
        if not existing:
            raise DiaryNotFoundError(diary_id=req.diary_id)

        old_rating = existing.rating

        dto = UpdateDiaryDTO(
            id=req.diary_id,
            rating=req.new_rating,
            date=req.date,
        )

        updated = await self._diary_repo.update(dto)

        return UpdateMoodResponse(
            success=True,
            diary_id=updated.id,
            old_rating=old_rating,
            new_rating=updated.rating,
        )
