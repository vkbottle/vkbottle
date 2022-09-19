import warnings
from typing import TYPE_CHECKING, Union, overload

from typing_extensions import Literal

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class AudioUploader(BaseUploader):
    NAME = "audio.mp3"

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("audio.getUploadServer", {}))["response"]

    @overload
    async def upload(
        self,
        artist: str,
        title: str,
        file_source: Union[str, "Bytes"],
        generate_attachment_strings: Literal[True] = ...,
        **params,
    ) -> str:
        ...

    @overload
    async def upload(
        self,
        artist: str,
        title: str,
        file_source: Union[str, "Bytes"],
        *,
        generate_attachment_strings: Literal[False],
        **params,
    ) -> dict:
        ...

    @overload
    async def upload(
        self,
        artist: str,
        title: str,
        file_source: Union[str, "Bytes"],
        generate_attachment_strings: bool = ...,
        **params,
    ) -> Union[str, dict]:
        ...

    async def upload(
        self,
        artist: str,
        title: str,
        file_source: Union[str, "Bytes"],
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
        server = await self.get_server()
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file})

        audio = (
            await self.api.request(
                "audio.save",
                {"artist": artist, "title": title, **uploader, **params},
            )
        )["response"]

        if self.generate_attachment_strings is not None:
            warnings.warn(
                "generate_attachment_strings in __init__ is deprecated"
                " pass this parameter directly to .upload()",
                DeprecationWarning,
            )
            generate_attachment_strings = self.generate_attachment_strings
        if generate_attachment_strings:
            return self.generate_attachment_string(
                "audio",
                await self.get_owner_id(params),
                audio["id"],
                audio.get("access_key"),
            )
        return audio

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME


__all__ = ("AudioUploader",)
