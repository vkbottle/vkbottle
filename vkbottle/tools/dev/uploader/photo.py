from abc import ABC
from typing import TYPE_CHECKING, List, Union

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class PhotoUploader(BaseUploader, ABC):
    NAME = "picture.jpg"

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME


class PhotoToAlbumUploader(PhotoUploader):
    async def upload(
        self, album_id: int, paths_like: Union[List[Union[str, "Bytes"]], str, "Bytes"], **params
    ) -> Union[str, List[Union[str, dict]]]:
        if not isinstance(paths_like, list):
            paths_like = [paths_like]

        server = await self.get_server(album_id=album_id, **params)
        files = {}

        for i, file_source in enumerate(paths_like):
            data = await self.read(file_source)
            files[f"file{i+1}"] = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], files)
        photos = (
            await self.api.request("photos.save", {"album_id": album_id, **uploader, **params})
        )["response"]

        if self.generate_attachment_strings:
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
    async def upload(self, file_source: Union[str, "Bytes"], **params) -> Union[str, List[dict]]:
        server = await self.get_server(**params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photos = (await self.api.request("photos.saveWallPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "photo", photos[0]["owner_id"], photos[0]["id"], photos[0].get("access_key")
            )
        return photos

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getWallUploadServer", {}))["response"]


class PhotoFaviconUploader(PhotoUploader):
    async def upload(self, file_source: Union[str, "Bytes"], **params) -> Union[str, dict]:
        owner_id = await self.get_owner_id(params)
        server = await self.get_server(owner_id=owner_id)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photo = (await self.api.request("photos.saveOwnerPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "wall", owner_id, photo["post_id"], photo.get("access_key")
            )
        return photo

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getOwnerPhotoUploadServer", kwargs))["response"]


class PhotoMessageUploader(PhotoUploader):
    async def upload(self, file_source: Union[str, "Bytes"], **params) -> Union[str, List[dict]]:
        server = await self.get_server(**params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photo = (await self.api.request("photos.saveMessagesPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "photo", photo[0]["owner_id"], photo[0]["id"], photo[0].get("access_key")
            )
        return photo

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getMessagesUploadServer", kwargs))["response"]


class PhotoChatFaviconUploader(PhotoUploader):
    async def upload(self, chat_id: int, file_source: Union[str, "Bytes"], **params) -> str:
        server = await self.get_server(chat_id=chat_id, **params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        return uploader["response"]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getChatUploadServer", kwargs))["response"]


class PhotoMarketUploader(PhotoUploader):
    async def upload(self, file_source: Union[str, "Bytes"], **params) -> dict:
        server = await self.get_server(**params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file})
        return (await self.api.request("photos.saveMarketPhoto", {**uploader, **params}))[
            "response"
        ]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getMarketUploadServer", kwargs))["response"]


__all__ = (
    "PhotoUploader",
    "PhotoToAlbumUploader",
    "PhotoWallUploader",
    "PhotoFaviconUploader",
    "PhotoMessageUploader",
    "PhotoChatFaviconUploader",
    "PhotoMarketUploader",
)
