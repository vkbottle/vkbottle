import typing
from ...framework import Bot, User
import aiohttp, json
import ssl


class Uploader:
    def __init__(
        self, vk: typing.Union[Bot, User], generate_attachment_strings: bool = False
    ):
        self.vk = vk
        self.user_instance = isinstance(vk, User)
        self.gas = generate_attachment_strings

    def get_group_id(self, group_id: int = None) -> int:
        return group_id if group_id is not None else getattr(self.vk, "group_id", False)

    def get_owner_id(self, group_id: int = None) -> int:
        group_id = self.get_group_id(group_id)
        return -group_id if group_id is not False else self.vk.user_id

    def client(self, vk: typing.Union[Bot, User]):
        return self.__class__(vk, self.gas)

    @staticmethod
    def open_pathlike(pathlike):
        if isinstance(pathlike, str):
            pathlike = open(pathlike, "rb")
        return pathlike

    @staticmethod
    async def upload(server: dict, files: dict, params: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                server["upload_url"], data=files, ssl=ssl.SSLContext(), params=params
            ) as response:
                uploader = json.loads(await response.text())
        return uploader

    @staticmethod
    def generate_attachment_string(segment: str, owner_id: int, id_: int) -> str:
        return "{segment}{owner_id}_{id_}".format(**locals())


class PhotoUploader(Uploader):
    async def upload_photo_to_album(
        self,
        album_id: int,
        pathlike: typing.Union[list, typing.Any],
        group_id: int = None,
        **params,
    ) -> typing.Union[str, typing.List[dict]]:

        if not isinstance(pathlike, list):
            pathlike = [pathlike]

        group_id = self.get_group_id(group_id)
        server = await self.vk.api.request(
            "photos.getUploadServer", {"album_id": album_id, "group_id": group_id}
        )
        files = dict()

        for i, file in enumerate(pathlike):
            files["file{}".format(i + 1)] = self.open_pathlike(file)

        uploader = await self.upload(server, files, params)

        photos = await self.vk.api.request(
            "photos.save",
            {"album_id": album_id, "group_id": group_id, **uploader, **params},
        )
        if self.gas:
            return [
                self.generate_attachment_string("photo", -group_id, photo["id"])
                for photo in photos
            ]
        return photos

    async def upload_wall_photo(self, pathlike, **params) -> typing.Union[str, dict]:
        server = await self.vk.api.request("photos.getWallUploadServer", {})
        uploader = await self.upload(
            server, {"photo": self.open_pathlike(pathlike)}, params
        )

        params = {**uploader, **params}
        photo = await self.vk.api.request("photos.saveWallPhoto", params)
        if self.gas:
            return self.generate_attachment_string(
                "photo", photo[0]["owner_id"], photo[0]["id"]
            )
        return photo

    async def update_favicon(self, pathlike, group_id: int = None, **params):
        server = await self.vk.api.request(
            "photos.getOwnerPhotoUploadServer",
            {"owner_id": self.get_owner_id(group_id)},
        )
        uploader = await self.upload(
            server, {"photo": self.open_pathlike(pathlike)}, params
        )
        photo = await self.vk.api.request("photos.saveOwnerPhoto", uploader)
        return photo

    async def upload_message_photo(self, pathlike, **params):
        server = await self.vk.api.request("photos.getMessagesUploadServer", params)
        uploader = await self.upload(
            server, {"photo": self.open_pathlike(pathlike)}, {}
        )

        photo = await self.vk.api.request("photos.saveMessagesPhoto", uploader)
        if self.gas:
            return self.generate_attachment_string(
                "photo", photo[0]["owner_id"], photo[0]["id"]
            )
        return photo

    async def upload_chat_favicon(self, pathlike, chat_id: int, **params) -> str:
        server = await self.vk.api.request(
            "photos.getChatUploadServer", dict(chat_id=chat_id, **params)
        )
        uploader = await self.upload(server, {"file": self.open_pathlike(pathlike)}, {})
        return uploader["response"]

    async def upload_market_photo(self, pathlike, **params):
        server = await self.vk.api.request("photos.getMarketUploadServer", params)
        uploader = await self.upload(server, {"file": self.open_pathlike(pathlike)}, {})

        photo = await self.vk.api.request("photos.saveMessagesPhoto", uploader)
        return await self.vk.api.request(
            "messages.setChatPhoto", {"file": photo["response"]}
        )
