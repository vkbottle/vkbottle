import typing
from vkbottle.framework import Bot, User
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

    def __repr__(self):
        return f"<{self.__class__.__name__} linked {self.vk.__class__.__name__}>"
