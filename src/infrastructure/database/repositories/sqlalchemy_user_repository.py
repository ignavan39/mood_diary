from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities import User
from domain.exceptions import DuplicateUserError
from domain.repositories.user_repository import UserRepository
from infrastructure.database.data_mappers import user_model_to_entity
from infrastructure.database.models import UserModel


class SQLAchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, user: User) -> User:
        user_model = UserModel(user_id=user.user_id, name=user.name)
        try:
            self.session.add(user_model)
            await self.session.refresh(user_model, attribute_names=["diaries"])
            return user_model_to_entity(user_model)
        except IntegrityError as e:
            await self.session.rollback()
            if 'unique constraint' in str(e.orig).lower():
                raise DuplicateUserError(user_id=user.user_id) from e
            raise
