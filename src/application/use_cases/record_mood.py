from dataclasses import dataclass
from datetime import date
from domain.entities import Diary
from domain.exceptions import DuplicateDiaryError
from domain.repositories import DiaryRepository, UserRepository


@dataclass
class RecordMoodRequest:
    external_user_id: int
    rating: int
    date: date


@dataclass
class RecordMoodResponse:
    success: bool
    is_existing: bool = False


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
                Diary(user_id=user.id, date=reg.date, rating=reg.rating)
            )
            return RecordMoodResponse(success=True,is_existing=False)

        except DuplicateDiaryError:
            return  RecordMoodResponse(success=False,is_existing=True)
        except:
            raise


