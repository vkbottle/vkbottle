from typing import TYPE_CHECKING, Any

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
        file_source: "str | Bytes | None" = None,
        link: str | None = None,
        name: str | None = None,
        description: str | None = None,
        is_private: bool | None = None,
        wallpost: bool | None = None,
        group_id: int | None = None,
        album_id: int | None = None,
        privacy_view: list[Any] | None = None,
        privacy_comment: list[Any] | None = None,
        no_comments: bool | None = None,
        repeat: bool | None = None,
        compression: bool | None = None,
        **params: Any,
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
        file_source: "str | Bytes | None" = None,
        link: str | None = None,
        name: str | None = None,
        description: str | None = None,
        is_private: bool | None = None,
        wallpost: bool | None = None,
        group_id: int | None = None,
        album_id: int | None = None,
        privacy_view: list[Any] | None = None,
        privacy_comment: list[Any] | None = None,
        no_comments: bool | None = None,
        repeat: bool | None = None,
        compression: bool | None = None,
        **params: Any,
    ) -> dict[str, Any]:
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

    async def get_server(self, **kwargs: Any) -> dict[str, Any]:
        return (await self.api.request("video.save", kwargs))["response"]


__all__ = ("VideoUploader",)
