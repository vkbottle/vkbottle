from typing import TYPE_CHECKING, List, Optional

from vkbottle.modules import json

from .button import KeyboardButton

if TYPE_CHECKING:
    from .action import ABCAction
    from .button import KeyboardButtonColor


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

    def add(
        self, action: "ABCAction", color: Optional["KeyboardButtonColor"] = None
    ) -> "Keyboard":
        if not len(self.buttons):
            self.row()
        button = KeyboardButton.from_typed(action, color)
        self.buttons[-1].append(button)
        return self

    def schema(self, rows: List[List[dict]]):
        for row in rows:
            self.row()
            for button in row:
                self.buttons[-1].append(KeyboardButton.from_dict(button))
        return self

    def get_json(self) -> str:
        data = json.dumps(
            {
                "one_time": self.one_time,
                "inline": self.inline,
                "buttons": [[button.get_data() for button in row] for row in self.buttons],
            }
        )

        if isinstance(data, bytes):
            return data.decode("utf-8")
        return data.encode("utf-8").decode("utf-8")

    def __str__(self) -> str:
        return self.get_json()
