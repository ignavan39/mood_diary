from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date as date_type

from .base import BaseModel


class DiaryModel(BaseModel):
    __tablename__ = "diaries"
    date: Mapped[date_type]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[int]
    __table_args__ = (
        Index("u_date_user", "date", "user_id"),
        UniqueConstraint("user_id", "date", name="idx_user_date"),
    )
