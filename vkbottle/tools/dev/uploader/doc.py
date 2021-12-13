from abc import ABC
from typing import TYPE_CHECKING, Union

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class DocUploader(BaseUploader, ABC):
    NAME = "doc.txt"

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("docs.getUploadServer", kwargs))["response"]

    async def upload(
        self, title: str, file_source: Union[str, "Bytes"], **params
    ) -> Union[str, dict]:
        server = await self.get_server(**params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data, name=title)

        uploader = await self.upload_files(server["upload_url"], {"file": file})

        doc = (
            await self.api.request(
                "docs.save",
                {"title": title, **uploader, **params},
            )
        )["response"]
        doc_type = doc["type"]

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                doc_type,
                doc[doc_type]["owner_id"],
                doc[doc_type]["id"],
                doc[doc_type].get("access_key"),
            )
        return doc

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME


class DocWallUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("docs.getWallUploadServer", kwargs))["response"]


class DocMessagesUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("docs.getMessagesUploadServer", kwargs))["response"]


class VoiceMessageUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return (
            await self.api.request(
                "docs.getMessagesUploadServer", {"type": "audio_message", **kwargs}
            )
        )["response"]


class GraffitiUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return (
            await self.api.request("docs.getMessagesUploadServer", {"type": "graffiti", **kwargs})
        )["response"]


__all__ = (
    "DocUploader",
    "DocWallUploader",
    "DocMessagesUploader",
    "VoiceMessageUploader",
    "GraffitiUploader",
)
