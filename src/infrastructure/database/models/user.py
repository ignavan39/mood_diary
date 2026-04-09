from typing import List
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .diary import DiaryModel


class UserModel(BaseModel):
    __tablename__ = "users"
    external_id: Mapped[str] = mapped_column(String(64), nullable=False)
    platform: Mapped[str] = mapped_column(
        String(32), nullable=False, default="telegram"
    )
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reminder_hour: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    reminder_enabled: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default="false"
    )
    diaries: Mapped[List["DiaryModel"]] = relationship(
        collection_class=list,
        cascade="delete, delete-orphan",
        passive_deletes=True,
    )
