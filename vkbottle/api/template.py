import typing
from .api import VKError
import json


class TemplateElement:
    def __init__(
        self,
        title: str = None,
        description: str = None,
        photo_id: str = None,
        buttons: typing.List[dict] = None,
        action: dict = None,
    ):
        if not buttons:
            raise VKError("Buttons are required")
        if not photo_id and not (title or description):
            raise VKError("photo_id or title is required")

        if type(buttons) is str:
            buttons = json.loads(buttons)

        buttons = buttons.get("buttons")[0]

        self.locals: typing.Dict = {
            k: v for k, v in locals().items() if v is not None and k != "self"
        }


def template_gen(*element: TemplateElement):
    return json.dumps({"type": "carousel", "elements": [e.locals for e in element]})
