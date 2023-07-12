from typing import TYPE_CHECKING, Literal, Union

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class SpeechUploader(BaseUploader):
    NAME = "voice.ogg"

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("asr.getUploadUrl", kwargs))["response"]

    async def raw_upload(
        self,
        file_source: Union[str, "Bytes"],
        model: Literal["neutral", "spontaneous"] = "neutral",
        **params,
    ) -> dict:
        server = await self.get_server(**params)
        data = await self.read(file_source)

        file = self.get_bytes_io(data, name=self.attachment_name)

        audio = await self.upload_files(server["upload_url"], {"file": file})

        return (
            await self.api.request(
                "asr.process",
                {"model": model, "audio": audio, **params},
            )
        )["response"]

    async def upload(
        self,
        **params,
    ) -> str:
        msg = f"{self.__class__.__name__} does not support upload() method. Use raw_upload(...) instead."
        raise NotImplementedError(msg)

    @property
    def attachment_name(self) -> str:
        return self._attachment_name or self.NAME
