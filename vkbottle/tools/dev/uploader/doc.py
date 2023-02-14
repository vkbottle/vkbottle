import os.path
from typing import TYPE_CHECKING, Optional, Union

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class DocUploader(BaseUploader):
    NAME = "doc.txt"

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("docs.getUploadServer", kwargs))["response"]

    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        **params,
    ) -> str:
        doc = await self.raw_upload(file_source, group_id, **params)
        doc_type = doc["type"]
        return self.generate_attachment_string(
            doc_type,
            doc[doc_type]["owner_id"],
            doc[doc_type]["id"],
            doc[doc_type].get("access_key"),
        )

    async def raw_upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        **params,
    ) -> dict:
        title = params.pop("title", None)
        if title is None:
            title = os.path.split(file_source)[1] if isinstance(file_source, str) else self.NAME
        server = await self.get_server(group_id=group_id, **params)
        data = await self.read(file_source)

        file = self.get_bytes_io(data, name=title)

        uploader = await self.upload_files(server["upload_url"], {"file": file})

        return (
            await self.api.request(
                "docs.save",
                {"title": title, **uploader, **params},
            )
        )["response"]

    @property
    def attachment_name(self) -> str:
        return self._attachment_name or self.NAME


class DocWallUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("docs.getWallUploadServer", kwargs))["response"]


class DocMessagesUploader(DocUploader):
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        peer_id: Optional[int] = None,
        **params,
    ) -> str:
        return await super().upload(
            file_source=file_source,
            group_id=group_id,
            peer_id=peer_id,
            **params,
        )

    async def raw_upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        peer_id: Optional[int] = None,
        **params,
    ) -> dict:
        return await super().raw_upload(
            file_source=file_source,
            group_id=group_id,
            peer_id=peer_id,
            **params,
        )

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
    "DocMessagesUploader",
    "DocUploader",
    "DocWallUploader",
    "GraffitiUploader",
    "VoiceMessageUploader",
)
