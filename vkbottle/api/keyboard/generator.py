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
            button = {k: v for k, v in button.items()}
            row_buttons.append(
                dict(
                    action=dict(
                        type=button.get("type", "text"),
                        label=button.get("text", button.get("label")),
                        **{
                            k: v
                            for k, v in button.items()
                            if k not in ["type", "text", "label", "color"]
                        }
                    ),
                    **(
                        {"color": button.get("color", "default")}
                        if button.get("type", "text") == "text"
                        else {}
                    )
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
