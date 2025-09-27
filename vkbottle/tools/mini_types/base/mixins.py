from typing import Protocol, List, Optional
from vkbottle_types.objects import (
    AudioAudio,
    DocsDoc,
    MessagesAudioMessage,
    PhotosPhoto,
    VideoVideoFull,
    WallWallComment,
    WallWallpostFull,
)
from vkbottle.modules import logger

class HasAttachments(Protocol):
    attachments: Optional[List]

class AttachmentMixin:
    def get_attachment_strings(self) -> Optional[List[str]]:
        if self.attachments is None:
            return None

        attachments = []
        for attachment in self.attachments:
            attachment_type = attachment.type.value
            attachment_object = getattr(attachment, attachment_type)
            if not hasattr(attachment_object, "id") or not hasattr(attachment_object, "owner_id"):
                logger.debug("Got unsupported attachment type: {}", attachment_type)
                continue

            attachment_string = (
                f"{attachment_type}{attachment_object.owner_id}_{attachment_object.id}"
            )
            if hasattr(attachment_object, "access_key"):
                attachment_string += f"_{attachment_object.access_key}"

            attachments.append(attachment_string)

        return attachments
    
    def get_wall_attachment(self) -> Optional[List["WallWallpostFull"]]:
        if self.attachments is None:
            return None
        result = [attachment.wall for attachment in self.attachments if attachment.wall]
        return result or None

    def get_wall_reply_attachment(self) -> Optional[List["WallWallComment"]]:
        if self.attachments is None:
            return None
        result = [
            attachment.wall_reply for attachment in self.attachments if attachment.wall_reply
        ]
        return result or None

    def get_photo_attachments(self) -> Optional[List["PhotosPhoto"]]:
        if self.attachments is None:
            return None
        return [attachment.photo for attachment in self.attachments if attachment.photo]

    def get_video_attachments(self) -> Optional[List["VideoVideoFull"]]:
        if self.attachments is None:
            return None
        return [attachment.video for attachment in self.attachments if attachment.video]

    def get_doc_attachments(self) -> Optional[List["DocsDoc"]]:
        if self.attachments is None:
            return None
        return [attachment.doc for attachment in self.attachments if attachment.doc]

    def get_audio_attachments(self) -> Optional[List["AudioAudio"]]:
        if self.attachments is None:
            return None
        return [attachment.audio for attachment in self.attachments if attachment.audio]

    def get_audio_message_attachments(self) -> Optional[List["MessagesAudioMessage"]]:
        if self.attachments is None:
            return None
        return [
            attachment.audio_message for attachment in self.attachments if attachment.audio_message
        ]

