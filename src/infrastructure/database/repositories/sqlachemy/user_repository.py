import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from domain.dtos import SaveUserDTO
from domain.entities import User
from domain.entities.user import Platform
from domain.exceptions import DuplicateUserError
from domain.repositories.user_repository import UserRepository
from infrastructure.database import DatabaseSessionManager
from infrastructure.database.models import UserModel
from infrastructure.database.utils import is_duplication_error

logger = logging.getLogger(__name__)


class SQLAchemyUserRepository(UserRepository):
    def __init__(self, session_manager: DatabaseSessionManager):
        self.async_session_maker = session_manager

    async def save(self, user: SaveUserDTO) -> User:
        async with self.async_session_maker.get_session() as session:
            user_model = UserModel(
                external_id=user.external_id,
                full_name=user.full_name,
                platform=user.platform,
                username=user.username,
            )

            try:
                session.add(user_model)
                await session.flush()
                return self._model_to_entity(user_model)

            except IntegrityError as e:
                if is_duplication_error(e):
                    raise DuplicateUserError(
                        user_id=user.external_id, platform=user.platform
                    ) from e
                raise
            except Exception:
                raise

    async def get_by_external_id(
        self, external_id: str, platfrom: Platform
    ) -> User | None:
        async with self.async_session_maker.get_session() as session:
            result = await session.execute(
                select(UserModel).where(
                    UserModel.external_id == external_id, UserModel.platform == platfrom
                )
            )
            user_model = result.scalar_one_or_none()

            if user_model is None:
                return None

            return self._model_to_entity(user_model)

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            full_name=model.full_name,
            external_id=model.external_id,
            platform=model.platform,  # type: ignore
            username=model.username,
        )
