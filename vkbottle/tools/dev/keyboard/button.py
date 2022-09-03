from typing import Any, Dict, Optional, Type

from .action import ABCAction, Callback, Location, OpenLink, Text, VKApps, VKPay
from .color import KeyboardButtonColor

KEYBOARD_ACTIONS = {
    "text": Text,
    "open_link": OpenLink,
    "callback": Callback,
    "location": Location,
    "vkpay": VKPay,
    "open_app": VKApps,
}


class KeyboardButton:
    def __init__(self, action: "ABCAction", color: Optional["KeyboardButtonColor"] = None):
        if not isinstance(action, ABCAction):
            raise TypeError("action must be instance of ABCAction")
        if color and not isinstance(color, KeyboardButtonColor):
            raise TypeError("color must be instance of KeyboardButtonColor")
        self.action = action
        self.color = color

    @classmethod
    def from_typed(
        cls: Type["KeyboardButton"],
        action: "ABCAction",
        color: Optional["KeyboardButtonColor"] = None,
    ) -> "KeyboardButton":
        return cls(action, color)

    @classmethod
    def from_dict(cls: Type["KeyboardButton"], data: dict) -> "KeyboardButton":
        action_type = KEYBOARD_ACTIONS.get(data.pop("type", None))
        color = data.pop("color", None)
        if color:
            color = KeyboardButtonColor(color)
        if action_type is None:
            raise ValueError("KeyboardButton action type is not defined")

        return cls(action_type(**data), color)

    def get_data(self) -> dict:
        data: Dict[str, Any] = {"action": self.action.get_data()}
        if self.action.type in ("text", "callback") and self.color:
            data["color"] = self.color.value
        return data
