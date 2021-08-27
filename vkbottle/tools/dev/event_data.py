from abc import ABC
from typing import Optional

from vkbottle.modules import json


class ABCEventData(ABC):
    type: str

    def get_data(self) -> dict:
        data = {k: v for k, v in vars(self).items() if v is not None}
        data["type"] = self.type
        return data

    def get_json(self) -> str:
        return json.dumps(self.get_data())

    def __str__(self):
        return self.get_json()


class ShowSnackbar(ABCEventData):
    type: str = "show_snackbar"

    def __init__(self, text: str):
        self.text = text


class OpenLink(ABCEventData):
    type: str = "open_link"

    def __init__(self, link: str):
        self.link = link


class OpenApp(ABCEventData):
    type: str = "open_app"

    def __init__(self, app_id: int, hash: str, owner_id: Optional[int] = None):
        self.app_id = app_id
        self.hash = hash
        self.owner_id = owner_id


__all__ = ("ABCEventData", "ShowSnackbar", "OpenLink", "OpenApp")
