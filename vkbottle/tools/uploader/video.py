from typing import TYPE_CHECKING, Optional, Union

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class VideoUploader(BaseUploader):
    NAME = "video.mp4"

    @property
    def attachment_name(self) -> str:
        return self._attachment_name or self.NAME

    async def upload(
        self,
        file_source: Optional[Union[str, "Bytes"]] = None,
        link: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_private: Optional[bool] = None,
        wallpost: Optional[bool] = None,
        group_id: Optional[int] = None,
        album_id: Optional[int] = None,
        privacy_view: Optional[list] = None,
        privacy_comment: Optional[list] = None,
        no_comments: Optional[bool] = None,
        repeat: Optional[bool] = None,
        compression: Optional[bool] = None,
        **params,
    ) -> str:
        server = await self.raw_upload(
            file_source=file_source,
            link=link,
            name=name,
            description=description,
            is_private=is_private,
            wallpost=wallpost,
            group_id=group_id,
            album_id=album_id,
            privacy_view=privacy_view,
            privacy_comment=privacy_comment,
            no_comments=no_comments,
            repeat=repeat,
            compression=compression,
            **params,
        )
        return self.generate_attachment_string(
            "video",
            server["owner_id"],
            server["video_id"],
        )

    async def raw_upload(
        self,
        file_source: Optional[Union[str, "Bytes"]] = None,
        link: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_private: Optional[bool] = None,
        wallpost: Optional[bool] = None,
        group_id: Optional[int] = None,
        album_id: Optional[int] = None,
        privacy_view: Optional[list] = None,
        privacy_comment: Optional[list] = None,
        no_comments: Optional[bool] = None,
        repeat: Optional[bool] = None,
        compression: Optional[bool] = None,
        **params,
    ) -> dict:
        server = await self.get_server(
            group_id=group_id,
            album_id=album_id,
            name=name,
            description=description,
            is_private=is_private,
            wallpost=wallpost,
            link=link,
            privacy_view=privacy_view,
            privacy_comment=privacy_comment,
            no_comments=no_comments,
            repeat=repeat,
            compression=compression,
        )
        if file_source is None and link is None:
            msg = "You must specify either file_source or link"
            raise ValueError(msg)

        if link:
            await self.api.http_client.request_json(server["upload_url"], method="GET")
        else:
            data = await self.read(file_source)  # type: ignore
            file = self.get_bytes_io(data)
            await self.upload_files(server["upload_url"], {"video_file": file}, **params)

        return server

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("video.save", kwargs))["response"]


__all__ = ("VideoUploader",)
