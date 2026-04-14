from typing import Any

Payload = str | dict[str, Any]


class ABCAction:
    type: str

    def get_data(self) -> dict[str, Any]:
        data = {k: v for k, v in vars(self).items() if v is not None}
        data["type"] = self.type
        return data


class Text(ABCAction):
    type = "text"

    def __init__(self, label: str, payload: Payload | None = None):
        self.label = label
        self.payload = payload


class OpenLink(ABCAction):
    type = "open_link"

    def __init__(self, link: str, label: str, payload: Payload | None = None):
        self.link = link
        self.label = label
        self.payload = payload


class Location(ABCAction):
    type = "location"

    def __init__(self, payload: Payload | None = None):
        self.payload = payload


class VKPay(ABCAction):
    type = "vkpay"

    def __init__(
        self,
        payload: Payload | None = None,
        hash: str | None = None,  # noqa: A002
    ):
        self.payload = payload
        self.hash = hash


class VKApps(ABCAction):
    type = "open_app"

    def __init__(
        self,
        app_id: int,
        owner_id: int,
        payload: Payload | None = None,
        label: str | None = None,
        hash: str | None = None,  # noqa: A002
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
    "Callback",
    "Location",
    "OpenLink",
    "Text",
    "VKApps",
    "VKPay",
)
