from vkbottle.api import API
from vkbottle.http import HTTPRequest
import aiohttp
from io import BytesIO
import json
import typing
import ssl


class Uploader:
    FILE_EXTENSIONS: typing.List[str] = []

    def __init__(self, api: API, generate_attachment_strings: bool = False):
        """ Uploader base
        :param api: API Instance
        :param generate_attachment_strings: return attachment short strings after upload
        """
        self.api = api
        self.http = HTTPRequest()
        self.gas = generate_attachment_strings

    async def get_group_id(self, group_id: int = None) -> int:
        return (
            group_id
            if group_id is not None
            else await getattr(self.api, "group_id", False)
        )

    async def get_data_from_link(
        self, link: str, ext: typing.Optional[str] = None
    ) -> BytesIO:
        content = BytesIO(await self.http.get(link, read_content=True))
        setattr(content, "name", f"file{self.file_extensions[0] or ext}")
        return content

    async def get_owner_id(self, group_id: int = None) -> int:
        group_id = await self.get_group_id(group_id)
        return -group_id if group_id is not False else await self.api.user_id

    def with_api(self, api: API) -> "Uploader":
        return self.__class__(api, self.gas)

    @staticmethod
    def open_pathlike(pathlike: typing.Union[str, BytesIO]) -> BytesIO:
        if isinstance(pathlike, str):
            return open(pathlike, "rb")
        pathlike.seek(0)
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

    @property
    def file_extensions(self) -> typing.List[str]:
        return self.FILE_EXTENSIONS

    def __repr__(self):
        return f"<{self.__class__.__name__} linked {self.api!r}>"
