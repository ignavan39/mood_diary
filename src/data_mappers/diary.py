

from entities.diary import Diary
from entities.user import User
from models.diary import DiaryModel


def diary_model_to_entity(instance: DiaryModel):
    return Diary(
        id=instance.id,
        date=instance.date,
        rating=instance.rating,
        user_id=instance.user_id,
    )


def diary_entity_to_model(diary: Diary) -> DiaryModel:
    return DiaryModel(
        id=diary.id, user_id=diary.user_id, date=diary.date, rating=diary.rating
    )
