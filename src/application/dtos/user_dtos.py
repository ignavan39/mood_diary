from dataclasses import dataclass


@dataclass
class UserBriefDTO:
    user_id: int
    name: str
    id: int
