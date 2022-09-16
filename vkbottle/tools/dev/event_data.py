from typing import Optional

from pydantic import BaseModel, Field


class ShowSnackbarEvent(BaseModel):
    type: str = Field(default="show_snackbar", const=True)
    text: str


class OpenLinkEvent(BaseModel):
    type: str = Field(default="open_link", const=True)
    link: str


class OpenAppEvent(BaseModel):
    type: str = Field(default="open_app", const=True)
    owner_id: Optional[int] = None
    app_id: int
    hash: str


__all__ = (
    "OpenAppEvent",
    "OpenLinkEvent",
    "ShowSnackbarEvent",
)
