from dataclasses import dataclass
from typing import Optional

from domain.entities.user import Platform


@dataclass
class SaveUserDTO:
    external_id: str
    full_name: Optional[str] = None
    platform: Platform = "telegram"
    username: Optional[str] = None
    reminder_hour: Optional[int] = None
    reminder_enabled: bool = False
