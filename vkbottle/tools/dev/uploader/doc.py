import os.path
import warnings
from typing import TYPE_CHECKING, Optional, Union, overload

from typing_extensions import Literal

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class DocUploader(BaseUploader):
    NAME = "doc.txt"

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("docs.getUploadServer", kwargs))["response"]

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        generate_attachment_strings: Literal[True] = ...,
        **params,
    ) -> str:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        generate_attachment_strings: Literal[False] = ...,
        **params,
    ) -> dict:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
        ...

    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
        title = params.pop("title", None)
        if title is None:
            if isinstance(file_source, str):
                title = os.path.split(file_source)[1]
            else:
                title = self.NAME
        server = await self.get_server(group_id=group_id, **params)
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
        if self.generate_attachment_strings is not None:
            warnings.warn(
                "generate_attachment_strings in __init__ is deprecated"
                " pass this parameter directly to .upload()",
                DeprecationWarning,
            )
            generate_attachment_strings = self.generate_attachment_strings
        if generate_attachment_strings:
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
    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = None,
        group_id: Optional[int] = None,
        generate_attachment_strings: Literal[True] = ...,
        **params,
    ) -> str:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = None,
        group_id: Optional[int] = None,
        *,
        generate_attachment_strings: Literal[False],
        **params,
    ) -> dict:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = None,
        group_id: Optional[int] = None,
        generate_attachment_strings: bool = ...,
        **params,
    ) -> Union[str, dict]:
        ...

    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = None,
        group_id: Optional[int] = None,
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
        return await super().upload(
            file_source=file_source,
            peer_id=peer_id,
            group_id=group_id,
            generate_attachment_strings=generate_attachment_strings,
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
