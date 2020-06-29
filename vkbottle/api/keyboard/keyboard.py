from .action import Text
from vkbottle.utils.exceptions import KeyboardError
from ...utils import except_none_self, json
import typing


class KeyboardButton:
    def __init__(self, action: typing.Union[Text], color: str = None):
        self.action = action or Text
        self.color = color or "default"

    def create(
        self,
        label: str = None,
        payload: str = None,
        link: str = None,
        hash: str = None,
        app_id: int = None,
        owner_id: int = None,
    ):
        self.action.__call__(**except_none_self(locals()))

    @property
    def json(self):
        return json.dumps(self.button)

    @property
    def button(self):
        b = {"action": except_none_self(self.action.dict())}
        if isinstance(self.action, Text):
            b["color"] = self.color
        return b


class Keyboard:
    def __init__(self, one_time: bool = False, inline: bool = False):
        self.buttons: typing.List[typing.List[KeyboardButton]] = []
        self.one_time: bool = one_time
        self.inline: bool = inline

    def row(self):
        if len(self.buttons) and not len(self.buttons[-1]):
            raise KeyboardError("Last row is empty!")
        self.buttons.append([])
        return self

    def add(self, action: typing.Union[Text], color: str = None):
        if not len(self.buttons):
            self.row()
        button = KeyboardButton(action, color)
        self.buttons[-1].append(button)
        return self

    def add_row(self):
        if len(self.buttons) and not len(self.buttons[-1]):
            raise KeyboardError("Last row is empty!")
        self.buttons.append([])

    def add_button(self, action: typing.Union[Text], color: str = None):
        if not len(self.buttons):
            raise KeyboardError("Firstly add row with keyboard.add_row()")
        button = KeyboardButton(action, color)
        self.buttons[-1].append(button)
        return button

    def generate(self):
        keyboard = {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": [[b.button for b in row] for row in self.buttons],
        }
        return json.dumps(keyboard)

    def __str__(self):
        return self.generate()

    def __repr__(self):
        return f"<Keyboard (generator) {len(self.buttons)} buttons>"
