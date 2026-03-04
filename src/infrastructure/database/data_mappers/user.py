from domain.entities import User
from infrastructure.database.data_mappers import diary_model_to_entity
from infrastructure.database.models import UserModel


def user_model_to_entity(model: UserModel) -> User:
    return User(
        user_id=model.user_id, name=model.name, diaries=[diary_model_to_entity(d) for d in model.diaries]
    )
