from ..base import BaseModel
from enum import IntEnum

from ..additional import PhotoSizes
from ..attachments import Graffiti, AudioMsg

# https://vk.com/dev/objects/doc


class DocumentType(IntEnum):
    text_document = 1
    archive = 2
    gif = 3
    image = 4
    audio = 5
    video = 6
    ebooks = 7
    unknown = 8


class DocumentPreview(BaseModel):
    photo: PhotoSizes = None
    graffiti: Graffiti = None
    audio_msg: AudioMsg = None


class Document(BaseModel):
    id: int = None
    owner_id: int = None
    title: str = None
    size: int = None
    ext: str = None
    url: str = None
    date: int = None
    type: DocumentType = None
    preview: DocumentPreview = None
    access_key: str = None
