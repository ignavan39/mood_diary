from sqlalchemy.orm import Session

from models.user import User as UserModel
from domain.repositories.user_repository import UserRepository


class SQLAchemyUserRepository(UserRepository):
    def __init__(self,session: Session) -> None:
        self.session = session
        
    def save(self, user: User) -> User:
        user_model = UserModel(
            user_id = user.user_id,
            name = user.name
        )