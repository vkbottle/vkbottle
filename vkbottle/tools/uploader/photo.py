from typing import TYPE_CHECKING, List, Optional, Union

from .base import BaseUploader

if TYPE_CHECKING:
    from .base import Bytes


class PhotoUploader(BaseUploader):
    NAME = "picture.jpg"

    @property
    def attachment_name(self) -> str:
        return self._attachment_name or self.NAME


class PhotoToAlbumUploader(PhotoUploader):
    MAX_PHOTOS_PER_UPLOAD = 5

    async def upload(
        self,
        album_id: int,
        paths_like: Union[List[Union[str, "Bytes"]], str, "Bytes"],
        group_id: Optional[int] = None,
        **params,
    ) -> List[str]:
        photos = await self.raw_upload(
            album_id=album_id,
            paths_like=paths_like,
            group_id=group_id,
            **params,
        )
        return [
            self.generate_attachment_string(
                "photo",
                photo["owner_id"],
                photo["id"],
                photo.get("access_key"),
            )
            for photo in photos
        ]

    async def raw_upload(
        self,
        album_id: int,
        paths_like: Union[List[Union[str, "Bytes"]], str, "Bytes"],
        group_id: Optional[int] = None,
        **params,
    ) -> List[dict]:
        if not isinstance(paths_like, list):
            paths_like = [paths_like]
        if len(paths_like) > self.MAX_PHOTOS_PER_UPLOAD:
            msg = "You can upload up to 5 photos at once"
            raise ValueError(msg)
        server = await self.get_server(album_id=album_id, group_id=group_id, **params)
        files = {}

        for i, file_source in enumerate(paths_like):
            data = await self.read(file_source)
            files[f"file{i + 1}"] = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], files)
        return (
            await self.api.request("photos.save", {"album_id": album_id, **uploader, **params})
        )["response"]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getUploadServer", kwargs))["response"]


class PhotoWallUploader(PhotoUploader):
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        **params,
    ) -> str:
        photo = await self.raw_upload(
            file_source=file_source,
            group_id=group_id,
            **params,
        )
        return self.generate_attachment_string(
            "photo",
            photo["owner_id"],
            photo["id"],
            photo.get("access_key"),
        )

    async def raw_upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: Optional[int] = None,
        **params,
    ) -> dict:
        server = await self.get_server(group_id=group_id, **params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        response = await self.api.request(
            "photos.saveWallPhoto",
            {
                "group_id": group_id,
                **uploader,
                **params,
            },
        )
        return response["response"][0]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getWallUploadServer", kwargs))["response"]


class PhotoFaviconUploader(PhotoUploader):
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        owner_id: Optional[int] = None,
        **params,
    ) -> str:
        owner_id = owner_id or await self.get_owner_id(**params)
        photo = await self.raw_upload(
            file_source=file_source,
            owner_id=owner_id,
            **params,
        )
        return self.generate_attachment_string(
            "wall",
            owner_id,
            photo["post_id"],
            photo.get("access_key"),
        )

    async def raw_upload(
        self,
        file_source: Union[str, "Bytes"],
        owner_id: Optional[int] = None,
        **params,
    ) -> dict:
        owner_id = owner_id or await self.get_owner_id(**params)
        server = await self.get_server(owner_id=owner_id)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        return (await self.api.request("photos.saveOwnerPhoto", {**uploader, **params}))[
            "response"
        ]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getOwnerPhotoUploadServer", kwargs))["response"]


class PhotoMessageUploader(PhotoUploader):
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = None,
        **params,
    ) -> str:
        photo = await self.raw_upload(
            file_source=file_source,
            peer_id=peer_id,
            **params,
        )
        return self.generate_attachment_string(
            "photo",
            photo["owner_id"],
            photo["id"],
            photo.get("access_key"),
        )

    async def raw_upload(
        self,
        file_source: Union[str, "Bytes"],
        peer_id: Optional[int] = None,
        **params,
    ) -> dict:
        server = await self.get_server(peer_id=peer_id, **params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        return (
            await self.api.request(
                "photos.saveMessagesPhoto",
                {**uploader, **params},
            )
        )[
            "response"
        ][0]

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getMessagesUploadServer", kwargs))["response"]


class PhotoChatFaviconUploader(PhotoUploader):
    async def upload(
        self,
        **params,
    ) -> str:
        msg = f"{self.__class__.__name__} does not support upload() method. Use raw_upload(...) instead."
        raise NotImplementedError(msg)

    async def raw_upload(
        self,
        chat_id: int,
        file_source: Union[str, "Bytes"],
        crop_x: Optional[int] = None,
        crop_y: Optional[int] = None,
        crop_width: Optional[int] = None,
        **params,
    ) -> dict:
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
        return await self.api.request(
            "photos.setChatPhoto", {"file": uploader["response"], **params}
        )

    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("photos.getChatUploadServer", kwargs))["response"]


class PhotoMarketUploader(PhotoUploader):
    async def upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: int,
        **params,
    ) -> str:
        photo = await self.raw_upload(
            file_source=file_source,
            group_id=group_id,
            **params,
        )
        return self.generate_attachment_string(
            "photo",
            photo["owner_id"],
            photo["id"],
            photo.get("access_key"),
        )

    async def raw_upload(
        self,
        file_source: Union[str, "Bytes"],
        group_id: int,
        **params,
    ) -> dict:
        server = await self.get_server(group_id=group_id, **params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file})
        return await self.api.request(
            "photos.saveMarketPhoto",
            {**uploader, **params},
        )

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
