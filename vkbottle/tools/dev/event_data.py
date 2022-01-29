from typing import ClassVar, Optional

from pydantic import BaseModel, Field


class ShowSnackbarEvent(BaseModel):
    type: ClassVar[str] = Field("show_snackbar", const=True)
    text: str


class OpenLinkEvent(BaseModel):
    type: ClassVar[str] = Field("open_link", const=True)
    link: str


class OpenAppEvent(BaseModel):
    type: ClassVar[str] = Field("open_app", const=True)
    owner_id: Optional[int] = None
    app_id: int
    hash: str


__all__ = ("ShowSnackbarEvent", "OpenLinkEvent", "OpenAppEvent")
