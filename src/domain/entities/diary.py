from dataclasses import dataclass
from datetime import date


@dataclass(kw_only=True)
class Diary:
    user_id: int
    date: date
    rating: int
