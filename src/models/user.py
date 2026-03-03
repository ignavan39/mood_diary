from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class User(Base):
	__tablename__ = "users"
	user_id: Mapped[int] = mapped_column(unique=True)
	name: Mapped[str | None]