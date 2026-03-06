from typing import List, Optional

from sqlalchemy import func, select
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

    async def get_stats_by_user_and_timerange(
        self,
        filters: DiaryFilter
    ) -> Optional[dict]:
        async with self.async_session_maker.get_session() as session:

          stmt = select(
              func.count(DiaryModel.id).label("total_entries"),
              func.avg(DiaryModel.rating).label("avg_mood"),
              func.min(DiaryModel.rating).label("min_mood"),
              func.max(DiaryModel.rating).label("max_mood"),
              func.max(DiaryModel.date).label("last_entry_date"),
          ).where(
              DiaryModel.user_id == filters.user_id,
              DiaryModel.created_at >= filters.start_date,
              DiaryModel.created_at <= filters.end_date,
          )

          result = await session.execute(stmt)
          row = result.first()

          if not row or row.total_entries == 0:
              return None

          return {
              "total": row.total_entries,
              "avg_mood": float(row.avg_mood) if row.avg_mood else 0.0,
              "min_mood": row.min_mood or 0,
              "max_mood": row.max_mood or 0,
          }

    def _model_to_entity(self, model: DiaryModel) -> Diary:
        return Diary(
            id=model.id,
            user_id=model.user_id,
            date=model.date,
            rating=model.rating,
        )
