import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from domain.entities import User
from domain.exceptions import DuplicateUserError
from domain.repositories.user_repository import UserRepository
from infrastructure.database import DatabaseSessionManager
from infrastructure.database.models import UserModel

logger = logging.getLogger(__name__)


class SQLAchemyUserRepository(UserRepository):
    def __init__(self, async_session_maker: DatabaseSessionManager):
        self.async_session_maker = async_session_maker

    async def save(self, user: User) -> User:
        async with self.async_session_maker.get_session() as session:
            user_model = UserModel(
                external_id=user.external_id,
                name=user.name,
            )

            try:
                session.add(user_model)
                await session.flush()
                return User(
                    id=user_model.id,
                    name=user_model.name,
                    external_id=user_model.external_id,
                )

            except IntegrityError as e:
                error_msg = str(e.orig).lower() if e.orig else str(e).lower()
                if "unique constraint" in error_msg or "duplicate key" in error_msg:
                    raise DuplicateUserError(user_id=user.external_id) from e
                raise
            except Exception:
                raise

    async def get_by_external_id(self, external_id: int) -> User | None:
        async with self.async_session_maker.get_session() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.external_id == external_id)
            )
            user_model = result.scalar_one_or_none()

            if user_model is None:
                return None

            return User(
                id=user_model.id,
                name=user_model.name,
                external_id=user_model.external_id,
            )
