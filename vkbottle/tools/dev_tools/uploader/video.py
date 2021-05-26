import json
from typing import Union, List, Optional

from .base import BaseUploader


class VideoUploader(BaseUploader):
    NAME = "video.mp4"

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME

    async def upload(
        self, file_source: Optional[Union[str, bytes]] = None, **params
    ) -> Union[str, List[dict], dict]:
        server = await self.get_server()
        assert (
            file_source is not None or "link" in params
        ), "file_source or link to video must be set"

        if "link" in params and not file_source:
            async with self.api.http as session:
                raw_response = await session.request_text(
                    "GET", server["upload_url"], params=params
                )
                return json.loads(raw_response)

        data = await self.read(file_source)  # type: ignore
        file = self.get_bytes_io(data)
        video = await self.upload_files(server["upload_url"], {"video_file": file})

        if self.generate_attachment_strings:
            return self.generate_attachment_string("video", video["owner_id"], video["id"])
        return video

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("video.save", kwargs))["response"]


__all__ = ("VideoUploader",)
