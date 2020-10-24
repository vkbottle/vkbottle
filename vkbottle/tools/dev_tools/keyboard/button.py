from .color import KeyboardButtonColor
from .action import ABCAction
from typing import Optional


class KeyboardButton:
    def __init__(self, action: ABCAction, color: Optional[KeyboardButtonColor] = None):
        self.action = action
        self.color = color

    def get_data(self) -> dict:
        data = {"action": self.action.get_data()}
        if self.action.type == "text" and self.color:
            data["color"] = self.color.value
        return data
