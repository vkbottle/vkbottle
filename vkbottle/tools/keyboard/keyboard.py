from typing import TYPE_CHECKING

from vkbottle.modules import json

from .button import KeyboardButton

if TYPE_CHECKING:
    from .action import ABCAction
    from .button import KeyboardButtonColor


class Keyboard:
    def __init__(self, one_time: bool = False, inline: bool = False):
        self.one_time = one_time
        self.inline = inline
        self.buttons: list[list[KeyboardButton]] = []
        self.expect_new_line = True

    def row(self) -> "Keyboard":
        self.buttons.append([])
        return self

    def add(self, action: "ABCAction", color: "KeyboardButtonColor | None" = None) -> "Keyboard":
        if not self.buttons:
            self.row()
        button = KeyboardButton.from_typed(action, color)
        self.buttons[-1].append(button)
        return self

    def schema(self, rows: list[list[dict]]):
        self.buttons += [[KeyboardButton.from_dict(button) for button in row] for row in rows]
        return self

    def get_json(self) -> str:
        buttons = [[button.get_data() for button in row] for row in self.buttons if row]
        data: str | bytes = json.dumps(
            {
                "one_time": self.one_time,
                "inline": self.inline,
                "buttons": buttons,
            }
        )
        return data.decode() if isinstance(data, bytes) else data

    def __str__(self) -> str:
        return self.get_json()
