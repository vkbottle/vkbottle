from abc import ABC, abstractmethod
from io import BytesIO
from typing import Optional, Callable, Union, Any

from vkbottle.api import ABCAPI
from vkbottle.modules import json

try:
    import aiofiles
except ImportError:
    aiofiles = None


class BaseUploader(ABC):
    def __init__(
        self,
        api: Optional[ABCAPI] = None,
        api_getter: Optional[Callable[[], ABCAPI]] = None,
        generate_attachment_strings: bool = True,
    ):
        assert api_getter is not None or api is not None, "api or api_getter should be set"
        self._get_api = api_getter or (lambda: api)  # type: ignore
        self.generate_attachment_strings = generate_attachment_strings

    @abstractmethod
    async def get_server(self, **kwargs) -> dict:
        pass

    @property
    @abstractmethod
    def attachment_name(self) -> str:
        pass

    @property
    def api(self) -> ABCAPI:
        return self._get_api()  # type: ignore

    async def upload_files(self, upload_url: str, files: dict, params: dict) -> dict:
        async with self.api.http as session:
            raw_response = await session.request_text(
                "POST", upload_url, data=files, params=params
            )
            response = json.loads(raw_response)
        return response

    def get_bytes_io(self, data: bytes) -> BytesIO:
        bytes_io = BytesIO(data)
        bytes_io.seek(0)  # To avoid errors with image generators (such as pillow)
        bytes_io.name = self.attachment_name  # To guarantee VK API file extension recognition
        return bytes_io

    async def get_owner_id(self, upload_params: dict) -> int:
        if "group_id" in upload_params:
            return upload_params["group_id"]
        return (await self.api.request("groups.getById", {}))["response"][0]["id"]

    @staticmethod
    def generate_attachment_string(attachment_type: str, owner_id: int, item_id: int) -> str:
        return f"{attachment_type}{owner_id}_{item_id}"

    @staticmethod
    async def read(path_like: Union[str, bytes]) -> bytes:
        if isinstance(path_like, str):
            assert aiofiles is not None, "to use default files opener aiofiles should be installed"
            async with aiofiles.open(path_like, "rb") as file:
                return await file.read()
        return path_like

    def __repr__(self) -> str:
        return f"<Uploader {self.__class__.__name__} with api {self.api!r}"
