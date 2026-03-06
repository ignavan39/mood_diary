import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from domain.entities import User
from domain.exceptions import DuplicateUserError
from domain.repositories.user_repository import UserRepository
from infrastructure.database import DatabaseSessionManager
from infrastructure.database.models import UserModel
from infrastructure.database.utils import is_duplication_error

logger = logging.getLogger(__name__)


class SQLAchemyUserRepository(UserRepository):
    def __init__(self, session_manager: DatabaseSessionManager):
        self.async_session_maker = session_manager

    async def save(self, user: User) -> User:
        async with self.async_session_maker.get_session() as session:
            user_model = UserModel(
                external_id=user.external_id,
                name=user.name,
            )

            try:
                session.add(user_model)
                await session.flush()
                return self._model_to_entity(user_model)

            except IntegrityError as e:
                if is_duplication_error(e):
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

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            external_id=model.external_id,
        )
