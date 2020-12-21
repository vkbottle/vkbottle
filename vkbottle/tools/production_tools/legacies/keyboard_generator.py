# type: ignore
# ^ ignore typing because legacies were entirely
# copied from vkbottle 2.x without quality insurance

from typing import List
from vkbottle.modules import json
from warnings import warn


def keyboard_gen(pattern: List[List[dict]], one_time: bool = False, inline: bool = False):
    """ Simple keyboard generator
    :param pattern: Keyboard simple pattern, check github readme
    :param one_time: Should keyboard be hidden after first use?
    :param inline: Should keyboard be inline?
    :return: VK Api Keyboard JSON
    """
    warn("keyboard_gen generator is obsolete, use Keyboard instead", DeprecationWarning)

    rows = pattern
    buttons = list()

    for row in rows:
        row_buttons = list()
        for button in row:
            action = dict()
            fields = dict()

            action["type"] = button.get("type", "text")
            action.update({k: v for k, v in button.items() if k not in ("type", "text", "color")})

            if action["type"] == "text":
                action["label"] = button.get("text", button.get("label"))
                fields["color"] = button.get("color", "default")

            row_button = {"action": action, **fields}

            row_buttons.append(row_button)
        buttons.append(row_buttons)

    keyboard = str(
        json.dumps(dict(one_time=one_time, buttons=buttons, inline=inline))
        .encode("utf-8")
        .decode("utf-8")
    )

    return keyboard
