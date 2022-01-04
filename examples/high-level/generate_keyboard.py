from vkbottle import Keyboard, KeyboardButtonColor, Text

# Simplest way of generating keyboard is non-builder interface
# Use <.row()> to add row
# Use <.add(Action(...), COLOR)> to add button to the last row
# Use <.get_json()> to make keyboard sendable
KEYBOARD_STANDARD = Keyboard(one_time=True, inline=False)
KEYBOARD_STANDARD.add(Text("Button 1"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_STANDARD.add(Text("Button 2"))
KEYBOARD_STANDARD.row()
KEYBOARD_STANDARD.add(Text("Button 3"))
KEYBOARD_STANDARD = KEYBOARD_STANDARD.get_json()  # type: ignore

# add and row methods returns the instance of Keyboard
# so, you can use it as builder
KEYBOARD_WITH_BUILDER = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Button 1"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Button 2"))
    .row()
    .add(Text("Button 3"))
    .get_json()
)

# Schema is another way to create keyboard
# all fields except of color are read as action fields
KEYBOARD_WITH_SCHEMA = (
    Keyboard(one_time=True, inline=False)
    .schema(
        [
            [
                {"label": "Button 1", "type": "text", "color": "positive"},
                {"label": "Button 2", "type": "text"},
            ],
            [{"label": "Button 3", "type": "text"}],
        ]
    )
    .get_json()
)

assert KEYBOARD_STANDARD == KEYBOARD_WITH_BUILDER == KEYBOARD_WITH_SCHEMA
