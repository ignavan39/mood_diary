from dataclasses import dataclass, field
from typing import List, Optional

from domain.entities.diary import Diary


@dataclass(kw_only=True)
class User:
    user_id: int
    name: Optional[str] = None
    diaries: List[Diary] = field(default_factory=list)
