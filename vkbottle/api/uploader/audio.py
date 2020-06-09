import typing
from io import BytesIO

from .base import Uploader


class AudioUploader(Uploader):
    FILE_EXTENSIONS = [".mp3", ".ogg", ".opus"]

    async def upload_audio(
        self, artist: str, title: str, pathlike: typing.Union[str, BytesIO], **params,
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

    async def upload_audio_message(
        self,
        pathlike: typing.Union[str, BytesIO],
        peer_id: int,
        doc_type: str = "audio_message",
        **params,
    ):
        server = await self.api.request(
            "docs.getMessagesUploadServer", {"type": doc_type, "peer_id": peer_id}
        )
        uploader = await self.upload(
            server, {"file": self.open_pathlike(pathlike)}, params
        )
        params = {**uploader, **params}
        doc = await self.api.request("docs.save", params)
        if self.gas:
            doc = doc[doc["type"]]
            return self.generate_attachment_string("doc", doc["owner_id"], doc["id"])
        return doc
