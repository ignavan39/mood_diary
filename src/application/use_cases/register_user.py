from dataclasses import dataclass
from typing import Optional

from domain.entities import User
from domain.exceptions import DuplicateUserError
from domain.repositories.user_repository import UserRepository


@dataclass
class RegisterUserRequest:
    external_id: int
    name: Optional[str] = None


@dataclass
class GetUserResponse:
    success: bool
    user: Optional[User] = None
    is_existing: bool = False


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def execute(self, reg: RegisterUserRequest):
        try:
            user = await self._user_repo.save(
                User(external_id=reg.external_id, name=reg.name)
            )
            return GetUserResponse(success=True, is_existing=False, user=user)
        except DuplicateUserError:
            return GetUserResponse(success=True, is_existing=True)
        except Exception:
            raise
