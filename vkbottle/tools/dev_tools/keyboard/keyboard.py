from vkbottle.modules import json
from .button import KeyboardButton, KeyboardButtonColor
from .action import ABCAction
from typing import List, Optional


class Keyboard:
    def __init__(self, one_time: bool = False, inline: bool = False):
        self.one_time = one_time
        self.inline = inline
        self.buttons: List[List[KeyboardButton]] = []

    def row(self) -> "Keyboard":
        if len(self.buttons) and not len(self.buttons[-1]):
            raise RuntimeError("Last row is empty!")
        self.buttons.append([])
        return self

    def add(self, action: ABCAction, color: Optional[KeyboardButtonColor] = None) -> "Keyboard":
        if not len(self.buttons):
            self.row()
        button = KeyboardButton(action, color)
        self.buttons[-1].append(button)
        return self

    def get_json(self) -> str:
        return json.dumps(
            {
                "one_time": self.one_time,
                "inline": self.inline,
                "buttons": [[button.get_data() for button in row] for row in self.buttons],
            }
        )

    def __str__(self) -> str:
        return self.get_json()
