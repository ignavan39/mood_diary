from dataclasses import dataclass, field
from typing import List, Literal, Optional

from mashumaro import DataClassDictMixin

from domain.entities.diary import Diary

Platform = Literal["telegram", "max", "vk"]


@dataclass
class User(DataClassDictMixin):
    external_id: str
    id: int
    full_name: Optional[str] = None
    platform: Platform = "telegram"
    username: Optional[str] = None
    diaries: List[Diary] = field(default_factory=list)
