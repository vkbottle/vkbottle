from typing import TYPE_CHECKING, Any, Union

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class AudioUploader(BaseUploader):
    NAME = "audio.mp3"

    async def get_server(self, **kwargs: Any) -> dict[str, Any]:
        return (await self.api.request("audio.getUploadServer", {}))["response"]

    async def upload(
        self,
        artist: str,
        title: str,
        file_source: Union[str, "Bytes"],
        **params: Any,
    ) -> str:
        audio = await self.raw_upload(artist, title, file_source, **params)
        return self.generate_attachment_string(
            "audio",
            await self.get_owner_id(**params, **audio),
            audio["id"],
            audio.get("access_key"),
        )

    async def raw_upload(
        self,
        artist: str,
        title: str,
        file_source: Union[str, "Bytes"],
        **params: Any,
    ) -> dict[str, Any]:
        server = await self.get_server()
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file})

        return (
            await self.api.request(
                "audio.save",
                {"artist": artist, "title": title, **uploader, **params},
            )
        )["response"]

    @property
    def attachment_name(self) -> str:
        return self._attachment_name or self.NAME


__all__ = ("AudioUploader",)
