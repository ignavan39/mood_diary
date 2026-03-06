from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass()
class Diary:
    id: Optional[int]
    user_id: int
    date: date
    rating: int
