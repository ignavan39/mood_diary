from dataclasses import dataclass
from datetime import date


@dataclass()
class Diary:
    user_id: int
    date: date
    rating: int
    id: int

    def __post_init__(self):
        if not 0 <= self.rating <= 10:
            raise ValueError("rating must be between 0 and 10")
