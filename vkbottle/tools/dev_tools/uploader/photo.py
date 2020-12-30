from abc import ABC
from typing import Union, List

from .base import BaseUploader, Bytes


class PhotoUploader(BaseUploader, ABC):
    NAME = "picture.jpg"

    @property
    def attachment_name(self) -> str:
        return self.NAME


class PhotoToAlbumUploader(PhotoUploader):
    async def upload(
        self, album_id: int, paths_like: Union[List[Union[str, Bytes]], str, Bytes], **params
    ) -> Union[str, List[Union[str, dict]]]:
        if not isinstance(paths_like, list):
            paths_like = [paths_like]

        server = await self.get_server()
        files = dict()

        for i, path_like in enumerate(paths_like):
            data = await self.read(path_like)
            files[f"file{i+1}"] = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], files, params)
        photos = (
            await self.api.request("photos.save", {"album_id": album_id, **uploader, **params})
        )["response"]

        if self.generate_attachment_strings:
            return [
                self.generate_attachment_string(
                    "photo", await self.get_owner_id(params), photo["id"]
                )
                for photo in photos
            ]
        return photos

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getUploadServer", kwargs))["response"]


class PhotoWallUploader(PhotoUploader):
    async def upload(self, path_like: Union[str, Bytes], **params) -> Union[str, List[dict]]:
        server = await self.get_server()
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file}, params)
        photos = (await self.api.request("photos.saveWallPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings:
            return self.generate_attachment_string("photo", photos[0]["owner_id"], photos[0]["id"])
        return photos

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getWallUploadServer", {}))["response"]


class PhotoFaviconUploader(PhotoUploader):
    async def upload(self, path_like: Union[str, Bytes], **params) -> Union[str, dict]:
        server = await self.get_server(owner_id=await self.get_owner_id(params))
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file}, params)
        photo = (await self.api.request("photos.saveOwnerPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "photo", await self.get_owner_id(params), photo["id"]
            )
        return photo

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getOwnerPhotoUploadServer", kwargs))["response"]


class PhotoMessageUploader(PhotoUploader):
    async def upload(self, path_like: Union[str, Bytes], **params) -> Union[str, List[dict]]:
        server = await self.get_server(**params)
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file}, params)
        photo = (await self.api.request("photos.saveMessagesPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings:
            return self.generate_attachment_string("photo", photo[0]["owner_id"], photo[0]["id"])
        return photo

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getMessagesUploadServer", kwargs))["response"]


class PhotoChatFaviconUploader(PhotoUploader):
    async def upload(self, chat_id: int, path_like: Union[str, Bytes], **params) -> str:
        server = await self.get_server(chat_id=chat_id, **params)
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file}, params)
        return uploader["response"]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getChatUploadServer", kwargs))["response"]


class PhotoMarketUploader(PhotoUploader):
    async def upload(self, path_like: Union[str, Bytes], **params) -> dict:
        server = await self.get_server(**params)
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file}, params)
        photo = (await self.api.request("photos.saveMarketPhoto", {**uploader, **params}))[
            "response"
        ]
        return photo

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
