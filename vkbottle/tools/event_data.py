from typing import Optional

from vkbottle.modules import pydantic


class ShowSnackbarEvent(pydantic.BaseModel):
    type: str = pydantic.Field(default="show_snackbar", const=True)
    text: str


class OpenLinkEvent(pydantic.BaseModel):
    type: str = pydantic.Field(default="open_link", const=True)
    link: str


class OpenAppEvent(pydantic.BaseModel):
    type: str = pydantic.Field(default="open_app", const=True)
    owner_id: Optional[int] = None
    app_id: int
    hash: str


__all__ = (
    "OpenAppEvent",
    "OpenLinkEvent",
    "ShowSnackbarEvent",
)
