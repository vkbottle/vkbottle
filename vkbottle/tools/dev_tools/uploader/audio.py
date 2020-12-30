from typing import Union

from .base import BaseUploader, Bytes


class AudioUploader(BaseUploader):
    NAME = "audio.mp3"

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("audio.getUploadServer", {}))["response"]

    async def upload(
        self, artist: str, title: str, path_like: Union[str, Bytes], **params
    ) -> Union[str, dict]:
        server = await self.get_server()
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file}, params)

        audio = (
            await self.api.request(
                "audio.save", {"artist": artist, "title": title, **uploader, **params},
            )
        )["response"]

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "audio", await self.get_owner_id(params), audio["id"]
            )
        return audio

    @property
    def attachment_name(self) -> str:
        return self.NAME


__all__ = ("AudioUploader",)
