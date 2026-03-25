import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ButtonColor(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class ButtonType(str, Enum):
    TEXT = "text"
    CALLBACK = "callback"
    URL = "open_link"
    LOCATION = "location"
    VK_PAY = "vkpay"
    VK_APPS = "open_app"


@dataclass(frozen=True)
class TextButton:
    label: str
    color: ButtonColor = ButtonColor.SECONDARY
    payload: Optional[dict[str, str]] = None

    def to_dict(self) -> dict:
        action: dict[str, str | dict[str, str]] = {
            "type": ButtonType.TEXT.value,
            "label": self.label,
        }
        if self.payload:
            action["payload"] = json.dumps(self.payload)

        result = {
            "action": action,
            "color": self.color.value,
        }
        return result


@dataclass(frozen=True)
class CallbackButton:
    label: str
    color: ButtonColor = ButtonColor.SECONDARY
    payload: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "action": {
                "type": ButtonType.CALLBACK.value,
                "label": self.label,
                "payload": json.dumps(self.payload),
            },
            "color": self.color.value,
        }


@dataclass(frozen=True)
class UrlButton:
    label: str
    url: str

    def to_dict(self) -> dict:
        return {
            "action": {
                "type": ButtonType.URL.value,
                "link": self.url,
                "label": self.label,
            },
        }


@dataclass
class VkKeyboard:
    """
    Builder клавиатур VK.

    Example:
        keyboard = (
            VkKeyboard()
            .add_text("Кнопка 1", color=ButtonColor.POSITIVE)
            .row()
            .add_text("Кнопка 2")
            .to_json()
        )
    """

    one_time: bool = False
    inline: bool = False
    buttons: list[list[dict]] = field(default_factory=list)
    _current_row: list[dict] = field(default_factory=list, repr=False)

    def _add_button(self, button_dict: dict) -> "VkKeyboard":
        self._current_row.append(button_dict)
        return self

    def _finish_row(self) -> "VkKeyboard":
        if self._current_row:
            self.buttons.append(list(self._current_row))
            self._current_row.clear()
        return self

    def add_text(
        self,
        label: str,
        color: ButtonColor = ButtonColor.SECONDARY,
        payload: Optional[dict[str, str]] = None,
    ) -> "VkKeyboard":
        button = TextButton(label=label, color=color, payload=payload)
        return self._add_button(button.to_dict())

    def add_callback(
        self,
        label: str,
        color: ButtonColor = ButtonColor.SECONDARY,
        payload: Optional[dict[str, str]] = None,
    ) -> "VkKeyboard":
        if not self.inline:
            raise ValueError("Callback buttons require inline=True")
        button = CallbackButton(label=label, color=color, payload=payload or {})
        return self._add_button(button.to_dict())

    def add_url(self, label: str, url: str) -> "VkKeyboard":
        button = UrlButton(label=label, url=url)
        return self._add_button(button.to_dict())

    def row(self) -> "VkKeyboard":
        return self._finish_row()

    def build(self) -> dict:
        self._finish_row()
        return {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": self.buttons,
        }

    def to_json(self, ensure_ascii: bool = False) -> str:
        return json.dumps(self.build(), ensure_ascii=ensure_ascii)

    def clear(self) -> "VkKeyboard":
        self.buttons.clear()
        self._current_row.clear()
        return self

    @classmethod
    def empty(cls) -> str:
        return json.dumps({"one_time": False, "inline": False, "buttons": []})


__all__ = [
    "ButtonColor",
    "ButtonType",
    "VkKeyboard",
    "TextButton",
    "CallbackButton",
    "UrlButton",
]
