import typing
from .base import Uploader
from io import BytesIO


class PhotoUploader(Uploader):
    FILE_EXTENSIONS = [".jpg", ".png", ".gif"]

    async def upload_photo_to_album(
        self,
        album_id: int,
        pathlike: typing.Union[str, BytesIO],
        group_id: int = None,
        **params,
    ) -> typing.Union[str, typing.List[str]]:

        if not isinstance(pathlike, list):
            pathlike = [pathlike]

        group_id = await self.get_group_id(group_id)
        server = await self.api.request(
            "photos.getUploadServer", {"album_id": album_id, "group_id": group_id}
        )
        files = dict()

        for i, file in enumerate(pathlike):
            files["file{}".format(i + 1)] = self.open_pathlike(file)

        uploader = await self.upload(server, files, params)

        photos = await self.api.request(
            "photos.save",
            {"album_id": album_id, "group_id": group_id, **uploader, **params},
        )
        if self.gas:
            return [
                self.generate_attachment_string("photo", -group_id, photo["id"])
                for photo in photos
            ]
        return photos

    async def upload_wall_photo(
        self, pathlike: typing.Union[str, BytesIO], **params
    ) -> typing.Union[str, dict]:
        server = await self.api.request("photos.getWallUploadServer", {})
        uploader = await self.upload(
            server, {"photo": self.open_pathlike(pathlike)}, params
        )

        params = {**uploader, **params}
        photo = await self.api.request("photos.saveWallPhoto", params)
        if self.gas:
            return self.generate_attachment_string(
                "photo", photo[0]["owner_id"], photo[0]["id"]
            )
        return photo

    async def update_favicon(
        self, pathlike: typing.Union[str, BytesIO], group_id: int = None, **params
    ):
        server = await self.api.request(
            "photos.getOwnerPhotoUploadServer",
            {"owner_id": self.get_owner_id(group_id)},
        )
        uploader = await self.upload(
            server, {"photo": self.open_pathlike(pathlike)}, params
        )
        photo = await self.api.request("photos.saveOwnerPhoto", uploader)
        return photo

    async def upload_message_photo(
        self, pathlike: typing.Union[str, BytesIO], **params
    ):
        server = await self.api.request("photos.getMessagesUploadServer", params)
        uploader = await self.upload(
            server, {"photo": self.open_pathlike(pathlike)}, {}
        )

        photo = await self.api.request("photos.saveMessagesPhoto", uploader)
        if self.gas:
            return self.generate_attachment_string(
                "photo", photo[0]["owner_id"], photo[0]["id"]
            )
        return photo

    async def upload_chat_favicon(
        self, pathlike: typing.Union[str, BytesIO], chat_id: int, **params
    ) -> str:
        server = await self.api.request(
            "photos.getChatUploadServer", dict(chat_id=chat_id, **params)
        )
        uploader = await self.upload(server, {"file": self.open_pathlike(pathlike)}, {})
        return uploader["response"]

    async def upload_market_photo(self, pathlike: typing.Union[str, BytesIO], **params):
        server = await self.api.request("photos.getMarketUploadServer", params)
        uploader = await self.upload(server, {"file": self.open_pathlike(pathlike)}, {})

        photo = await self.api.request("photos.saveMessagesPhoto", uploader)
        return await self.api.request(
            "messages.setChatPhoto", {"file": photo["response"]}
        )
