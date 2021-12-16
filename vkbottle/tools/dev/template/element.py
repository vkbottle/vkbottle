from typing import List, Optional, Union

from vkbottle.modules import json


class TemplateElement:
    """Easy template element generator"""

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        photo_id: Optional[str] = None,
        buttons: Optional[Union[List[dict], str]] = None,
        action: Optional[dict] = None,
    ):
        assert buttons, "Buttons are required"
        assert photo_id or title, "photo_id or title is required"

        if isinstance(buttons, str):
            buttons = json.loads(buttons)

        if isinstance(buttons, dict):
            buttons = buttons.get("buttons")[0]  # taking only first row

        self.raw: dict = {k: v for k, v in locals().items() if v is not None and k != "self"}
