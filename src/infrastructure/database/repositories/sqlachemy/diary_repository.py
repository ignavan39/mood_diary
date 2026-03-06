from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from domain.entities import Diary
from domain.exceptions import DuplicateDiaryError
from domain.repositories import DiaryRepository
from domain.repositories.diary_repository import DiaryFilter
from infrastructure.database import DatabaseSessionManager
from infrastructure.database.models import DiaryModel
from infrastructure.database.utils import is_duplication_error


class SQLAchemyDiaryRepository(DiaryRepository):
    def __init__(self, session_manager: DatabaseSessionManager):
        self.async_session_maker = session_manager

    async def save(self, diary: Diary) -> Diary | None:
        async with self.async_session_maker.get_session() as session:
            diaryModel = DiaryModel(
                user_id=diary.user_id, rating=diary.rating, date=diary.date
            )
            try:
                session.add(diaryModel)
                await session.flush()
                return self._model_to_entity(diaryModel)
            except IntegrityError as e:
                if is_duplication_error(e):
                    raise DuplicateDiaryError(user_id=diary.user_id, date=diary.date)
                raise
            except Exception:
                raise

    async def get_many_by_user_and_timerange(self, filters: DiaryFilter) -> List[Diary]:
        async with self.async_session_maker.get_session() as session:
            stmt = select(DiaryModel).where(DiaryModel.user_id == filters.user_id)

            if filters.start_date:
                stmt = stmt.where(DiaryModel.date >= filters.start_date)

            if filters.end_date:
                stmt = stmt.where(DiaryModel.date <= filters.end_date)

            stmt = stmt.order_by(DiaryModel.date.desc())

            if filters.limit:
                stmt = stmt.limit(filters.limit)

            result = await session.execute(stmt)
            models = result.scalars().all()

            return [self._model_to_entity(m) for m in models]

    def _model_to_entity(self, model: DiaryModel) -> Diary:
        return Diary(
            id=model.id,
            user_id=model.user_id,
            date=model.date,
            rating=model.rating,
        )
