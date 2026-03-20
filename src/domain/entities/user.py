from dataclasses import dataclass, field
from typing import List, Literal, Optional

from domain.entities.diary import Diary

Platform = Literal["telegram", "max", 'vk']


@dataclass
class User:
    external_id: str
    id: int
    full_name: Optional[str] = None
    platform: Platform = "telegram"
    username: Optional[str] = None
    diaries: List[Diary] = field(default_factory=list)
