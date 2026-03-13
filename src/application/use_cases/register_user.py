from dataclasses import dataclass
from typing import Optional

from domain.dtos import SaveUserDTO
from domain.entities import User
from domain.entities.user import Platform
from domain.exceptions import DuplicateUserError
from domain.repositories.user_repository import UserRepository


@dataclass
class RegisterUserRequest:
    platform: Platform
    external_user_id: str
    full_name: Optional[str] = None
    username: Optional[str] = None


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
                SaveUserDTO(
                    external_id=reg.external_user_id,
                    platform=reg.platform,
                    full_name=reg.full_name,
                    username=reg.username,
                )
            )
            return GetUserResponse(success=True, is_existing=False, user=user)
        except DuplicateUserError:
            return GetUserResponse(success=True, is_existing=True)
        except Exception:
            raise
