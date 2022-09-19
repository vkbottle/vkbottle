import warnings
from typing import TYPE_CHECKING, Optional, Union, overload

from typing_extensions import Literal

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class VideoUploader(BaseUploader):
    NAME = "video.mp4"

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME

    @overload
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
        generate_attachment_strings: Literal[True] = True,
        **params,
    ) -> str:
        ...

    @overload
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
        generate_attachment_strings: Literal[False] = ...,
        **params,
    ) -> dict:
        ...

    @overload
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
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
        ...

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
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
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
            raise ValueError("You must specify either file_source or link")

        if link:
            await self.api.http_client.request_json(server["upload_url"], method="GET")
        else:
            data = await self.read(file_source)  # type: ignore
            file = self.get_bytes_io(data)
            await self.upload_files(server["upload_url"], {"video_file": file}, **params)

        if self.generate_attachment_strings is not None:
            warnings.warn(
                "generate_attachment_strings in __init__ is deprecated"
                " pass this parameter directly to .upload()",
                DeprecationWarning,
            )
            generate_attachment_strings = self.generate_attachment_strings
        if generate_attachment_strings:
            return self.generate_attachment_string("video", server["owner_id"], server["video_id"])
        return server

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("video.save", kwargs))["response"]


__all__ = ("VideoUploader",)
