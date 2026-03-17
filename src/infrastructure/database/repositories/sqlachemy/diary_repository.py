from datetime import date, datetime, timedelta
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from domain.dtos import SaveDiaryDTO, UpdateDiaryDTO
from domain.entities import Diary, StatsPeriod
from domain.exceptions import DuplicateDiaryError
from domain.exceptions.exceptions import DiaryNotFoundError
from domain.repositories import DiaryRepository
from domain.repositories.diary_repository import DiaryFilter
from infrastructure.database import DatabaseSessionManager
from infrastructure.database.models import DiaryModel
from infrastructure.database.utils import is_duplication_error


class SQLAchemyDiaryRepository(DiaryRepository):
    def __init__(self, session_manager: DatabaseSessionManager):
        self.async_session_maker = session_manager

    async def save(self, diary: SaveDiaryDTO) -> Diary | None:
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
                    existing = await self.get_by_user_and_date(
                        diary.user_id, diary.date
                    )

                    if existing is None:
                        raise DiaryNotFoundError()

                    raise DuplicateDiaryError(
                        diary_id=existing.id,
                        user_id=diary.user_id,
                        date=diary.date,
                        rating=diary.rating,
                    )
                raise
            except Exception:
                raise

    async def get_stats_by_user_and_timerange(
        self, filters: DiaryFilter
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

    async def get_stats_by_user(
        self,
        user_id: int,
        period: StatsPeriod,
    ) -> Optional[dict]:
        async with self.async_session_maker.get_session() as session:
            end_date = datetime.now().date()

            if period == StatsPeriod.ALL:
                start_date = None
            else:
                start_date = end_date - timedelta(days=period.value)

            stmt = select(
                func.count(DiaryModel.id).label("total_entries"),
                func.avg(DiaryModel.rating).label("avg_mood"),
                func.min(DiaryModel.rating).label("min_mood"),
                func.max(DiaryModel.rating).label("max_mood"),
                func.max(DiaryModel.date).label("last_entry_date"),
                func.min(DiaryModel.date).label("first_entry_date"),
            ).where(DiaryModel.user_id == user_id)

            if start_date:
                stmt = stmt.where(DiaryModel.date >= start_date)

            stmt = stmt.where(DiaryModel.date <= end_date)

            result = await session.execute(stmt)
            row = result.first()
            if not row or row.total_entries == 0:
                return None
            return {
                "total_entries": row.total_entries,
                "avg_mood": float(row.avg_mood) if row.avg_mood else 0.0,
                "min_mood": row.min_mood or 0,
                "max_mood": row.max_mood or 0,
                "last_entry_date": row.last_entry_date,
                "first_entry_date": row.first_entry_date,
            }

    async def update(self, diary: UpdateDiaryDTO) -> Diary:
        async with self.async_session_maker.get_session() as session:
            stmt = select(DiaryModel).where(DiaryModel.id == diary.id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if not model:
                raise DiaryNotFoundError(diary.id)

            fields = diary.get_fields_to_update()

            for field_name, value in fields.items():
                setattr(model, field_name, value)

            await session.flush()
            await session.refresh(model)

            return self._model_to_entity(model)

    async def get_by_id(self, diary_id: int) -> Optional[Diary]:
        async with self.async_session_maker.get_session() as session:
            stmt = select(DiaryModel).where(DiaryModel.id == diary_id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            return self._model_to_entity(model) if model else None

    async def get_by_user_and_date(self, user_id: int, date: date) -> Optional[Diary]:
        async with self.async_session_maker.get_session() as session:
            stmt = select(DiaryModel).where(
                DiaryModel.user_id == user_id,
                DiaryModel.date == date,
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            return self._model_to_entity(model) if model else None

    def _model_to_entity(self, model: DiaryModel) -> Diary:
        return Diary(
            id=model.id,
            user_id=model.user_id,
            date=model.date,
            rating=model.rating,
        )

    async def get_many_by_user_and_timerange(
        self,
        filters: DiaryFilter,
    ) -> List[Diary]:
        async with self.async_session_maker.get_session() as session:
            stmt = select(DiaryModel).where(DiaryModel.user_id == filters.user_id)

            if filters.start_date:
                stmt = stmt.where(DiaryModel.date >= filters.start_date)

            if filters.end_date:
                stmt = stmt.where(DiaryModel.date <= filters.end_date)

            if filters.limit:
                stmt = stmt.limit(filters.limit)

            if filters.offset:
                stmt = stmt.offset(filters.offset)

            if filters.order_by == "date_desc":
                stmt = stmt.order_by(DiaryModel.date.desc())
            else:
                stmt = stmt.order_by(DiaryModel.date.asc())

            result = await session.execute(stmt)
            models = result.scalars().all()
            return [self._model_to_entity(model) for model in models]
