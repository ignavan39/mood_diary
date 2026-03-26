from dataclasses import dataclass
from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class LongPollEventProto(Protocol):
    type: int
    t: int
    raw: dict[str, Any]
    user_id: Optional[int]
    peer_id: Optional[int]
    text: Optional[str]
    from_me: Optional[bool]


@runtime_checkable
class VkUserProto(Protocol):
    id: int
    first_name: str
    last_name: str


@dataclass(frozen=True)
class VkUser:
    id: int
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def mention(self) -> str:
        return f"[id{self.id}|{self.full_name}]"


@dataclass(frozen=True)
class VkMessage:
    from_user: VkUser
    peer_id: int
    text: str
    timestamp: int
    payload: Optional[dict[str, Any]] = None
    event_id: Optional[str] = None
    @property
    def is_private(self) -> bool:
        return self.peer_id == self.from_user.id

    def to_log_dict(self) -> dict[str, Any]:
        return {
            "from": self.from_user.full_name,
            "text": self.text[:100],
            "private": self.is_private,
        }


@dataclass
class VkEvent:
    type: int
    object: dict[str, Any]
    group_id: int
    timestamp: int

    @classmethod
    def from_longpoll(cls, event: LongPollEventProto, group_id: int) -> "VkEvent":
        return cls(
            type=event.type,
            object=event.raw.get("object", {}),
            group_id=group_id,
            timestamp=event.t,
        )

    @classmethod
    def to_message(cls, event: LongPollEventProto) -> Optional[VkMessage]:
        if event.user_id is None or event.peer_id is None:
            return None

        return VkMessage(
            from_user=VkUser(
                id=event.user_id,
                first_name="",
                last_name="",
            ),
            peer_id=event.peer_id,
            text=event.text or "",
            timestamp=event.t,
            payload=event.raw.get("object", {}).get("payload"),
        )


__all__ = [
    "LongPollEventProto",
    "VkUserProto",
    "VkUser",
    "VkMessage",
    "VkEvent",
]
