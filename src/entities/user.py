from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from .diary import Diary

@dataclass(kw_only=True)
class User:
    user_id: int
    name: Optional[str] = None
    diaries: List[Diary] = field(default_factory=list)
