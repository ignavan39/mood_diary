from datetime import date


class DomainException(Exception):
    pass


class DuplicateUserError(DomainException):
    def __init__(self, user_id: int, message: str = "User already exists"):
        self.user_id = user_id
        super().__init__(f"{message}: user_id={user_id}")


class DuplicateDiaryError(DomainException):
    def __init__(self, user_id: int, date: date, message: str = "Diary already exists"):
        self.user_id = user_id
        super().__init__(f"{message}: user_id={user_id} date={date}")
