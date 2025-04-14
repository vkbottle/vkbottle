from typing import Optional

import pydantic


class ShowSnackbarEvent(pydantic.BaseModel):
    type: str = pydantic.Field(default="show_snackbar", frozen=True)
    text: str


class OpenLinkEvent(pydantic.BaseModel):
    type: str = pydantic.Field(default="open_link", frozen=True)
    link: str


class OpenAppEvent(pydantic.BaseModel):
    type: str = pydantic.Field(default="open_app", frozen=True)
    owner_id: Optional[int] = None
    app_id: int
    hash: str


__all__ = (
    "OpenAppEvent",
    "OpenLinkEvent",
    "ShowSnackbarEvent",
)
