from abc import ABC
from typing import Union

from .base import BaseUploader, Bytes


class DocUploader(BaseUploader, ABC):
    NAME = "doc.txt"

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("docs.getUploadServer", kwargs))["response"]

    async def upload(self, title: str, path_like: Union[str, Bytes], **params) -> Union[str, dict]:
        server = await self.get_server()
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file}, params)

        doc = (
            await self.api.request(
                "docs.save",
                {"title": title, **uploader, **params},
            )
        )["response"]

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "doc", await self.get_owner_id(params), doc["id"]
            )
        return doc

    @property
    def attachment_name(self) -> str:
        return self.NAME


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
