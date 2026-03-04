from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities import User


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        """Persist a user and return it with generated ID"""
        pass

    # @abstractmethod
    # def find_by_id(self, user_id: int) -> Optional[User]:
    #     """Find user by ID"""
    #     pass

    # @abstractmethod
    # def find_by_email(self, email: str) -> Optional[User]:
    #     """Find user by email"""
    #     pass

    # @abstractmethod
    # def find_all(self) -> List[User]:
    #     """Get all users"""
    #     pass

    # @abstractmethod
    # def delete(self, user_id: int) -> bool:
    #     """Delete user by ID"""
    #     pass
