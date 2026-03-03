from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date as date_type

from models.user import User
from models.base import Base


class Diary(Base):
	__tablename__ = "diaries"
	date: Mapped[date_type] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),primary_key=True)
	rating: Mapped[int]
	user: Mapped["User"] = relationship(
    "User",
    back_populates="diaries"
  )