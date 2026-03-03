from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .diary import DiaryModel


class UserModel(BaseModel):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str | None]
    diaries: Mapped[List["DiaryModel"]] = relationship(
        back_populates="user",
        collection_class=list,
        cascade="delete, delete-orphan",
        passive_deletes=True,
    )
