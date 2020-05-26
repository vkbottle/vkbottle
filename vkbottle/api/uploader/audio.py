import typing
from .base import Uploader


class AudioUploader(Uploader):
    FILE_EXTENSIONS = [".mp3", ".ogg", ".opus"]

    async def upload_audio(
        self,
        artist: str,
        title: str,
        pathlike: typing.Union[str, typing.Any],
        **params,
    ) -> typing.Union[str, dict]:

        server = await self.api.request("audio.getUploadServer", {})

        file = self.open_pathlike(pathlike)
        uploader = await self.upload(server, {"file": file}, params)

        audio = await self.api.request(
            "audio.save", {"artist": artist, "title": title, **uploader, **params},
        )
        if self.gas:
            return self.generate_attachment_string(
                "audio", await self.api.user_id, audio["id"]
            )
        return audio
