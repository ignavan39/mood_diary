from dataclasses import dataclass

from domain.entities import User


@dataclass
class UserContext:
    user: User
    is_existing: bool


@dataclass
class Context:
    user_ctx: UserContext
