from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date as date_type

from models.base import BaseModel


class DiaryModel(BaseModel):
    __tablename__ = "diaries"
    date: Mapped[date_type] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    rating: Mapped[int]
