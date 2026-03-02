from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
	__tablename__ = "users"
	id: Mapped[int] = mapped_column(unique=True)
	name: Mapped[str | None]