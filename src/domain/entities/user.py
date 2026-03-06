from dataclasses import dataclass, field
from typing import List, Optional

from domain.entities.diary import Diary


@dataclass
class User:
    external_id: int
    id: Optional[int] = None
    name: Optional[str] = None
    diaries: List[Diary] = field(default_factory=list)
