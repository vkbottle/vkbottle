from typing import Optional

from .action import ABCAction
from .color import KeyboardButtonColor


class KeyboardButton:
    def __init__(
        self, action: ABCAction, color: KeyboardButtonColor, data: dict,
    ):
        self.action = action
        self.color = color
        self.data = data

    @classmethod
    def from_typed(cls, action: ABCAction, color: Optional[KeyboardButtonColor] = None):
        return cls(action, color, None)  # type: ignore

    @classmethod
    def from_dict(cls, data: dict):
        color = data.get("color")
        data = {"action": data}
        if color is not None:
            data["action"].pop("color")
            data["color"] = color
        return cls(None, None, data)  # type: ignore

    def get_data(self) -> dict:
        if self.data is not None:
            return self.data

        data = {"action": self.action.get_data()}
        if self.action.type in ("text", "callback",) and self.color:
            data["color"] = self.color.value
        return data
