from domain.entities.diary import Diary
from infrastructure.database.models import DiaryModel


def diary_model_to_entity(instance: DiaryModel):
    return Diary(
        date=instance.date,
        rating=instance.rating,
        user_id=instance.user_id,
    )
