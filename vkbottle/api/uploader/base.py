from vkbottle.api import API
import aiohttp, json
import ssl


class Uploader:
    def __init__(self, api: API, generate_attachment_strings: bool = False):
        """ Uploader base
        :param api: API Instance
        :param generate_attachment_strings: return attachment short strings after upload
        """
        self.api = api
        self.gas = generate_attachment_strings

    async def get_group_id(self, group_id: int = None) -> int:
        return (
            group_id
            if group_id is not None
            else await getattr(self.api, "group_id", False)
        )

    async def get_owner_id(self, group_id: int = None) -> int:
        group_id = await self.get_group_id(group_id)
        return -group_id if group_id is not False else await self.api.user_id

    def with_api(self, api: API):
        return self.__class__(api, self.gas)

    @staticmethod
    def open_pathlike(pathlike):
        if isinstance(pathlike, str):
            return open(pathlike, "rb")
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
    def generate_attachment_string(segment: str, owner_id: int, item_id: int) -> str:
        return "{segment}{owner_id}_{item_id}".format(**locals())

    def __repr__(self):
        return f"<{self.__class__.__name__} linked {self.api!r}>"
