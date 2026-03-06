from dataclasses import dataclass


@dataclass
class UserBriefDTO:
    external_id: int
    name: str
    id: int
