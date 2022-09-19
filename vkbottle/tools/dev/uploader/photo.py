import warnings
from typing import TYPE_CHECKING, List, Optional, Union, overload

from typing_extensions import Literal

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class PhotoUploader(BaseUploader):
    NAME = "picture.jpg"

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME


class PhotoToAlbumUploader(PhotoUploader):
    @overload
    async def upload(
        self,
        album_id: int,
        paths_like: Union[List[Union[str, "Bytes"]], str, "Bytes"],
        group_id: Optional[int] = ...,
        generate_attachment_strings: Literal[True] = ...,
        **params,
    ) -> List[str]:
        ...

    @overload
    async def upload(
        self,
        album_id: int,
        paths_like: Union[List[Union[str, "Bytes"]], str, "Bytes"],
        group_id: Optional[int] = ...,
        generate_attachment_strings: Literal[False] = ...,
        **params,
    ) -> List[dict]:
        ...

    @overload
    async def upload(
        self,
        album_id: int,
        paths_like: Union[List[Union[str, "Bytes"]], str, "Bytes"],
        group_id: Optional[int] = ...,
        generate_attachment_strings: bool = ...,
        **params,
    ) -> Union[List[str], List[dict]]:
        ...

    async def upload(
        self,
        album_id: int,
        paths_like: Union[List[Union[str, "Bytes"]], str, "Bytes"],
        group_id: Optional[int] = None,
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[List[str], List[dict]]:
        if not isinstance(paths_like, list):
            paths_like = [paths_like]
        if len(paths_like) > 5:
            raise ValueError("You can upload up to 5 photos at once")
        server = await self.get_server(album_id=album_id, group_id=group_id, **params)
        files = {}

        for i, file_source in enumerate(paths_like):
            data = await self.read(file_source)
            files[f"file{i+1}"] = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], files)
        photos = (
            await self.api.request("photos.save", {"album_id": album_id, **uploader, **params})
        )["response"]

        if self.generate_attachment_strings is not None:
            warnings.warn(
                "generate_attachment_strings in __init__ is deprecated"
                " pass this parameter directly to .upload()",
                DeprecationWarning,
            )
            generate_attachment_strings = self.generate_attachment_strings
        if generate_attachment_strings:
            return [
                self.generate_attachment_string(
                    "photo", photo["owner_id"], photo["id"], photo.get("access_key")
                )
                for photo in photos
            ]
        return photos

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getUploadServer", kwargs))["response"]


class PhotoWallUploader(PhotoUploader):
    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = ...,
        generate_attachment_strings: Literal[True] = ...,
        **params,
    ) -> str:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = ...,
        generate_attachment_strings: Literal[False] = ...,
        **params,
    ) -> dict:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = ...,
        generate_attachment_strings: bool = ...,
        **params,
    ) -> Union[str, dict]:
        ...

    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
        server = await self.get_server(group_id=group_id, **params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photos = (await self.api.request("photos.saveWallPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings is not None:
            warnings.warn(
                "generate_attachment_strings in __init__ is deprecated"
                " pass this parameter directly to .upload()",
                DeprecationWarning,
            )
            generate_attachment_strings = self.generate_attachment_strings
        if generate_attachment_strings:
            return self.generate_attachment_string(
                "photo", photos[0]["owner_id"], photos[0]["id"], photos[0].get("access_key")
            )
        return photos[0]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getWallUploadServer", {}))["response"]


class PhotoFaviconUploader(PhotoUploader):
    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        owner_id: Optional[int] = ...,
        generate_attachment_strings: Literal[True] = ...,
        **params,
    ) -> str:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        owner_id: Optional[int] = ...,
        generate_attachment_strings: Literal[False] = ...,
        **params,
    ) -> dict:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        owner_id: Optional[int] = ...,
        generate_attachment_strings: bool = ...,
        **params,
    ) -> Union[str, dict]:
        ...

    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        owner_id: Optional[int] = None,
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
        owner_id = owner_id or await self.get_owner_id(params)
        server = await self.get_server(owner_id=owner_id)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photo = (await self.api.request("photos.saveOwnerPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings is not None:
            warnings.warn(
                "generate_attachment_strings in __init__ is deprecated"
                " pass this parameter directly to .upload()",
                DeprecationWarning,
            )
            generate_attachment_strings = self.generate_attachment_strings
        if generate_attachment_strings:
            return self.generate_attachment_string(
                "wall", owner_id, photo["post_id"], photo.get("access_key")
            )
        return photo

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getOwnerPhotoUploadServer", kwargs))["response"]


class PhotoMessageUploader(PhotoUploader):
    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = ...,
        generate_attachment_strings: Literal[True] = ...,
        **params,
    ) -> str:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = ...,
        generate_attachment_strings: Literal[False] = ...,
        **params,
    ) -> dict:
        ...

    @overload
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = ...,
        generate_attachment_strings: bool = ...,
        **params,
    ) -> Union[str, dict]:
        ...

    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = None,
        generate_attachment_strings: bool = True,
        **params,
    ) -> Union[str, dict]:
        server = await self.get_server(peer_id=peer_id, **params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photo = (await self.api.request("photos.saveMessagesPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings is not None:
            warnings.warn(
                "generate_attachment_strings in __init__ is deprecated"
                " pass this parameter directly to .upload()",
                DeprecationWarning,
            )
            generate_attachment_strings = self.generate_attachment_strings
        if generate_attachment_strings:
            return self.generate_attachment_string(
                "photo", photo[0]["owner_id"], photo[0]["id"], photo[0].get("access_key")
            )
        return photo

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getMessagesUploadServer", kwargs))["response"]


class PhotoChatFaviconUploader(PhotoUploader):
    async def upload(
        self,
        chat_id: int,
        file_source: Union[str, "Bytes"],
        crop_x: Optional[int] = None,
        crop_y: Optional[int] = None,
        crop_width: Optional[int] = None,
        **params,
    ) -> str:
        server = await self.get_server(
            chat_id=chat_id,
            crop_x=crop_x,
            crop_y=crop_y,
            crop_width=crop_width,
            **params,
        )
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        return uploader["response"]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getChatUploadServer", kwargs))["response"]


class PhotoMarketUploader(PhotoUploader):
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: int,
        **params,
    ) -> dict:
        server = await self.get_server(group_id=group_id, **params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file})
        return (
            await self.api.request(
                "photos.saveMarketPhoto",
                {**uploader, **params},
            )
        )["response"]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getMarketUploadServer", kwargs))["response"]


__all__ = (
    "PhotoChatFaviconUploader",
    "PhotoFaviconUploader",
    "PhotoMarketUploader",
    "PhotoMessageUploader",
    "PhotoToAlbumUploader",
    "PhotoUploader",
    "PhotoWallUploader",
)
