from . import base, photos
import typing
from enum import Enum
from ..base import BaseModel


class Doc(BaseModel):
    access_key: str = None
    date: int = None
    ext: str = None
    id: int = None
    is_licensed: "base.BoolInt" = None
    owner_id: int = None
    preview: "DocPreview" = None
    size: int = None
    title: str = None
    type: int = None
    url: str = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class DocAttachmentType(Enum):
    doc = "doc"
    graffiti = "graffiti"
    audio_message = "audio_message"


class DocPreview(BaseModel):
    photo: "DocPreviewPhoto" = None
    video: "DocPreviewVideo" = None


class DocPreviewPhoto(BaseModel):
    sizes: typing.List["photos.PhotoSizes"] = None


class DocPreviewVideo(BaseModel):
    filesize: int = None
    height: int = None
    src: str = None
    width: int = None


class DocTypes(BaseModel):
    count: int = None
    id: int = None
    title: str = None


class DocUploadResponse(BaseModel):
    file: str = None


Doc.update_forward_refs()
DocPreview.update_forward_refs()
DocPreviewPhoto.update_forward_refs()
DocPreviewVideo.update_forward_refs()
DocTypes.update_forward_refs()
DocUploadResponse.update_forward_refs()
