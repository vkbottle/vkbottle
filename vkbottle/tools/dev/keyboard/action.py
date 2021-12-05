from abc import ABC
from typing import Optional, Union

Payload = Union[str, dict]


class ABCAction(ABC):
    type: str

    def get_data(self) -> dict:
        data = {k: v for k, v in vars(self).items() if v is not None}
        data["type"] = self.type
        return data


class Text(ABCAction):
    type = "text"

    def __init__(self, label: str, payload: Optional[Payload] = None):
        self.label = label
        self.payload = payload


class OpenLink(ABCAction):
    type = "open_link"

    def __init__(self, link: str, label: str, payload: Optional[Payload] = None):
        self.link = link
        self.label = label
        self.payload = payload


class Location(ABCAction):
    type = "location"

    def __init__(self, payload: Optional[Payload] = None):
        self.payload = payload


class VKPay(ABCAction):
    type = "vkpay"

    def __init__(self, payload: Optional[Payload] = None, hash: Optional[str] = None):
        self.payload = payload
        self.hash = hash


class VKApps(ABCAction):
    type = "open_app"

    def __init__(
        self,
        app_id: int,
        owner_id: int,
        payload: Optional[Payload] = None,
        label: Optional[str] = None,
        hash: Optional[str] = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id
        self.payload = payload
        self.label = label
        self.hash = hash


class Callback(ABCAction):
    type = "callback"

    def __init__(self, label: str, payload: Payload):
        self.label = label
        self.payload = payload


__all__ = (
    "ABCAction",
    "Text",
    "OpenLink",
    "Location",
    "VKPay",
    "VKApps",
    "Callback",
)
