from typing import List, Optional, Union

from vkbottle.modules import json
from vkbottle.tools.dev.keyboard import Keyboard
from vkbottle.tools.dev.keyboard.button import KeyboardButton


class TemplateElement:
    """Easy template element generator"""

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        photo_id: Optional[str] = None,
        buttons: Union[List[KeyboardButton], List[dict], str, None] = None,
        action: Optional[dict] = None,
    ):
        assert buttons, "Buttons are required"
        assert photo_id or title, "photo_id or title is required"

        if isinstance(buttons, str):
            buttons = json.loads(buttons)["buttons"][0]  # type: ignore

        if isinstance(buttons, dict):
            buttons = buttons["buttons"][0]  # type: ignore

        if isinstance(buttons, Keyboard):
            buttons = [button.get_data() for button in buttons.buttons[0]]

        if all(isinstance(button, KeyboardButton) for button in buttons):  # type: ignore
            buttons = [button.get_data() for button in buttons]  # type: ignore
        self.raw: dict = {k: v for k, v in locals().items() if v is not None and k != "self"}
