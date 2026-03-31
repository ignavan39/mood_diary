from dataclasses import dataclass
from typing import Optional

from domain.dtos import SaveUserDTO
from domain.entities import User
from domain.entities.user import Platform
from domain.exceptions import DuplicateUserError, UserNotFoundError
from domain.repositories.user_repository import UserRepository


@dataclass
class EnsureUserRequest:
    platform: Platform
    external_user_id: str
    full_name: Optional[str] = None
    username: Optional[str] = None


@dataclass
class EnsureUserResponse:
    success: bool
    user: User
    is_existing: bool = False


class EnsureUserUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, reg: EnsureUserRequest) -> EnsureUserResponse:
        try:
            user = await self._user_repo.save(
                SaveUserDTO(
                    external_id=reg.external_user_id,
                    platform=reg.platform,
                    full_name=reg.full_name,
                    username=reg.username,
                )
            )
            return EnsureUserResponse(success=True, is_existing=False, user=user)
        except DuplicateUserError:
            user_exist = await self._user_repo.get_by_external_id(
                external_id=reg.external_user_id, platfrom=reg.platform
            )
            if user_exist is None:
                raise UserNotFoundError(external_user_id=str(reg.external_user_id))

            return EnsureUserResponse(success=True, is_existing=True, user=user_exist)
        except Exception:
            raise
