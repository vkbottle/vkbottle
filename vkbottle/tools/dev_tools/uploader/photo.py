from abc import ABC
from typing import List, Union

from .base import BaseUploader


class PhotoUploader(BaseUploader, ABC):
    NAME = "picture.jpg"

    @property
    def attachment_name(self) -> str:
        return self.NAME

    async def upload_photo_to_ulbum(
        self, album_id: int, paths_like: Union[List[Union[str, bytes]], str, bytes], **params
    ) -> Union[str, List[Union[str, dict]]]:
        if not isinstance(paths_like, list):
            paths_like = [paths_like]

        server = (await self.api.request("photos.getUploadServer", params))["response"]
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

    async def upload_wall_photo(
        self, path_like: Union[str, bytes], **params
    ) -> Union[str, List[dict]]:
        server = (await self.api.request("photos.getWallUploadServer", {}))["response"]
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file}, params)
        photos = (await self.api.request("photos.saveWallPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings:
            return self.generate_attachment_string("photo", photos[0]["owner_id"], photos[0]["id"])
        return photos

    async def upload_favicon(self, path_like: Union[str, bytes], **params) -> Union[str, dict]:
        server = (
            await self.api.request(
                "photos.getOwnerPhotoUploadServer", {"owner_id": await self.get_owner_id(params)}
            )
        )["response"]
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

    async def upload_message_photo(
        self, path_like: Union[str, bytes], **params
    ) -> Union[str, List[dict]]:
        server = (await self.api.request("photos.getMessagesUploadServer", params))["response"]
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file}, params)
        photo = (await self.api.request("photos.saveMessagesPhoto", {**uploader, **params}))[
            "response"
        ]

        if self.generate_attachment_strings:
            return self.generate_attachment_string("photo", photo[0]["owner_id"], photo[0]["id"])
        return photo

    async def upload_chat_favicon(
        self, chat_id: int, path_like: Union[str, bytes], **params
    ) -> str:
        server = (await self.api.request("photos.getChatUploadServer", params))["response"]
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file}, params)
        return uploader["response"]

    async def upload_photo_to_market(self, path_like: Union[str, bytes], **params) -> dict:
        server = await (await self.api.request("photos.getMarketUploadServer", params))["response"]
        data = await self.read(path_like)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file}, params)
        photo = (await self.api.request("photos.saveMarketPhoto", {**uploader, **params}))[
            "response"
        ]
        return photo


__all__ = ("PhotoUploader",)
