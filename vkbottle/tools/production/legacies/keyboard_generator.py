from typing import List
from warnings import warn

from vkbottle.modules import json


def keyboard_gen(pattern: List[List[dict]], one_time: bool = False, inline: bool = False):
    """Simple keyboard generator
    :param pattern: Keyboard simple pattern, check github readme
    :param one_time: Should keyboard be hidden after first use?
    :param inline: Should keyboard be inline?
    :return: VK Api Keyboard JSON
    """
    warn("keyboard_gen generator is obsolete, use Keyboard instead", DeprecationWarning)

    rows = pattern
    buttons = []

    for row in rows:
        row_buttons = []
        for button in row:
            action = {}
            fields = {}

            action["type"] = button.get("type", "text")
            action.update({k: v for k, v in button.items() if k not in ("type", "text", "color")})

            if action["type"] == "text":
                action["label"] = button.get("text", button.get("label"))

            if button.get("color"):
                fields["color"] = button["color"]

            row_button = {"action": action, **fields}

            row_buttons.append(row_button)
        buttons.append(row_buttons)

    return str(
        json.dumps(dict(one_time=one_time, inline=inline, buttons=buttons))
        .encode("utf-8")
        .decode("utf-8")
    )
