from dataclasses import dataclass
from datetime import date as date_type


@dataclass
class SaveDiaryDTO:
    user_id: int
    rating: int
    date: date_type
