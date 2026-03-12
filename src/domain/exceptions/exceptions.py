from datetime import date
from typing import Optional


class DomainException(Exception):
    pass


class DuplicateUserError(DomainException):
    def __init__(self, user_id: int, message: str = "User already exists"):
        self.user_id = user_id
        super().__init__(f"{message}: user_id={user_id}")


class UserNotFoundError(DomainException):
    def __init__(
        self, external_user_id: Optional[int] = None, message: str = "User not found"
    ):
        self.external_user_id = external_user_id
        super().__init__(f"{message}: external_user_id={external_user_id}")


class DuplicateDiaryError(DomainException):
    def __init__(
        self,
        diary_id: int,
        user_id: int,
        date: date,
        rating: int,
        message: str = "Diary already exists",
    ):
        self.user_id = user_id
        self.diary_id = diary_id
        self.rating = rating
        super().__init__(
            f"{message}: diary_id={diary_id} user_id={user_id} date={date}"
        )


class DiaryNotFoundError(DomainException):
    def __init__(
        self, diary_id: Optional[int] = None, message: str = "Diary not found"
    ):
        self.diary_id = diary_id
        super().__init__(f"{message}: diary_id={diary_id}")


class InvalidDiaryRatingError(DomainException):
    def __init__(
        self,
        rating: int,
        message: str = "Ivalid rating",
    ):
        super().__init__(f"{message}: rating={rating}")
