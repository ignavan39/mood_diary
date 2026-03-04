import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities import User
from domain.exceptions import DuplicateUserError
from domain.repositories.user_repository import UserRepository
from infrastructure.database.data_mappers import user_model_to_entity
from infrastructure.database.models import UserModel

logger = logging.getLogger(__name__)


class SQLAchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        user_model = UserModel(
            user_id=user.user_id,
            name=user.name,
        )

        try:
            self.session.add(user_model)
            await self.session.flush()
            return user_model_to_entity(user_model)

        except IntegrityError as e:
            error_msg = str(e.orig).lower() if e.orig else str(e).lower()
            if "unique constraint" in error_msg or "duplicate key" in error_msg:
                raise DuplicateUserError(user_id=user.user_id) from e
            raise

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return user_model_to_entity(model)
