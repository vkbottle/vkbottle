from typing import List, Dict

try:
    import ujson as json
except ImportError:
    import json


def keyboard_gen(
    pattern: List[List[Dict]], one_time: bool = False, inline: bool = False
):
    """Simple keyboard constructor
    :param pattern: Keyboard simple pattern, check github readme
    :param one_time: Should keyboard be hidden after first use?
    :return: VK Api Keyboard JSON
    """
    rows = pattern
    buttons = list()
    for row in rows:
        row_buttons = list()
        for button in row:
            row_buttons.append(
                dict(
                    action=dict(
                        type="text" if "type" not in button else button["type"],
                        label=button["text"],
                        payload=json.dumps(
                            "" if "payload" not in button else button["payload"]
                        ),
                    ),
                    color="default" if "color" not in button else button["color"],
                )
            )
        buttons.append(row_buttons)

    keyboard = str(
        json.dumps(
            dict(one_time=one_time, buttons=buttons, inline=inline), ensure_ascii=False
        )
        .encode("utf-8")
        .decode("utf-8")
    )

    return keyboard
