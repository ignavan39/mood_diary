from dataclasses import dataclass
from datetime import date
from typing import Optional
from domain.dtos import SaveDiaryDTO
from domain.exceptions import DuplicateDiaryError
from domain.repositories import DiaryRepository, UserRepository


@dataclass
class RecordMoodRequest:
    external_user_id: int
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

    async def execute(self, reg: RecordMoodRequest):
        user = await self._user_repo.get_by_external_id(
            external_id=reg.external_user_id
        )
        if user is None or user.id is None:
            return RecordMoodResponse(success=False)

        try:
            await self._diary_repo.save(
                SaveDiaryDTO(user_id=user.id, date=reg.date, rating=reg.rating)
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
