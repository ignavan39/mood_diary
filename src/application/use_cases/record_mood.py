from dataclasses import dataclass
from datetime import date
from typing import Optional
from domain.dtos import SaveDiaryDTO
from domain.entities.user import Platform
from domain.exceptions import (
    DuplicateDiaryError,
    InvalidDiaryRatingError,
    UserNotFoundError,
)
from domain.repositories import DiaryRepository, UserRepository


@dataclass
class RecordMoodRequest:
    platform: Platform
    external_user_id: str
    rating: int
    date: date


@dataclass
class ExistDiary:
    existing_diary_id: int
    old_rating: int


@dataclass
class RecordMoodResponse:
    success: bool
    exist_diary: Optional[ExistDiary] = None
    needs_confirmation: bool = False


class RecordMoodUseCase:
    def __init__(self, diary_repo: DiaryRepository, user_repo: UserRepository):
        self._diary_repo = diary_repo
        self._user_repo = user_repo

    async def execute(self, req: RecordMoodRequest):
        user = await self._user_repo.get_by_external_id(
            external_id=req.external_user_id, platfrom=req.platform
        )
        if user is None:
            user_id = user.id if user is not None else None
            raise UserNotFoundError(external_user_id=user_id)

        if req.rating < 0 or req.rating > 10:
            raise InvalidDiaryRatingError(rating=req.rating)

        try:
            await self._diary_repo.save(
                SaveDiaryDTO(user_id=user.id, date=req.date, rating=req.rating)
            )
            return RecordMoodResponse(success=True, needs_confirmation=False)

        except DuplicateDiaryError as e:
            return RecordMoodResponse(
                success=False,
                exist_diary=ExistDiary(
                    existing_diary_id=e.diary_id, old_rating=e.rating
                ),
                needs_confirmation=True,
            )
        except:
            raise
