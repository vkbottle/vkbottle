from vkbottle.utils.exceptions import TemplateError
from vkbottle.utils.json import json
import typing


class CarouselEl:
    def __init__(
        self,
        title: str = None,
        description: str = None,
        photo_id: str = None,
        buttons: typing.List[dict] = None,
        action: dict = None,
    ):
        if not buttons:
            raise TemplateError("Buttons are required")
        if not photo_id and not (title or description):
            raise TemplateError("photo_id or title is required")

        if isinstance(buttons, str):
            buttons = json.loads(buttons)

        if isinstance(buttons, dict):
            buttons = buttons.get("buttons")[0]  # taking only first row

        self.raw: typing.Dict = {
            k: v for k, v in locals().items() if v is not None and k != "self"
        }
