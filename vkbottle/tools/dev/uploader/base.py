from abc import ABC, abstractmethod
from io import BytesIO
from typing import TYPE_CHECKING, Callable, Optional, Union

import aiofiles

from vkbottle.exception_factory.base_exceptions import VKAPIError
from vkbottle.modules import json

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI

    Bytes = Union[bytes, BytesIO]


class BaseUploader(ABC):
    def __init__(
        self,
        api: Optional["ABCAPI"] = None,
        api_getter: Optional[Callable[[], "ABCAPI"]] = None,
        generate_attachment_strings: bool = True,
        with_name: Optional[str] = None,
    ):
        assert api_getter is not None or api is not None, "api or api_getter should be set"
        self._get_api = api_getter or (lambda: api)  # type: ignore
        self.generate_attachment_strings = generate_attachment_strings
        self.with_name = with_name

    @abstractmethod
    async def get_server(self, **kwargs) -> dict:
        pass

    @property
    @abstractmethod
    def attachment_name(self) -> str:
        pass

    @property
    def api(self) -> "ABCAPI":
        return self._get_api()  # type: ignore

    async def upload_files(self, upload_url: str, files: dict) -> dict:
        raw_response = await self.api.http_client.request_text(
            upload_url, method="POST", data=files
        )
        return json.loads(raw_response)

    def get_bytes_io(self, data: "Bytes", name: str = None) -> BytesIO:
        bytes_io = data if isinstance(data, BytesIO) else BytesIO(data)
        bytes_io.seek(0)  # To avoid errors with image generators (such as pillow)
        bytes_io.name = (
            name or self.attachment_name
        )  # To guarantee VK API file extension recognition
        return bytes_io

    async def get_owner_id(self, upload_params: dict) -> int:
        if "group_id" in upload_params:
            return upload_params["group_id"]
        if "user_id" in upload_params:
            return upload_params["user_id"]
        if "owner_id" in upload_params:
            return upload_params["owner_id"]
        try:
            return (await self.api.request("groups.getById", {}))["response"][0]["id"]
        except VKAPIError:
            return (await self.api.request("users.get", {}))["response"][0]["id"]

    @staticmethod
    def generate_attachment_string(
        attachment_type: str, owner_id: int, item_id: int, access_key: Optional[str] = None
    ) -> str:
        return f"{attachment_type}{owner_id}_{item_id}{('_' + access_key) if access_key else ''}"

    @staticmethod
    async def read(file_source: Union[str, "Bytes"]) -> "Bytes":
        if isinstance(file_source, str):
            async with aiofiles.open(file_source, "rb") as file:
                return await file.read()
        return file_source

    def __repr__(self) -> str:
        return f"<Uploader {self.__class__.__name__} with api {self.api!r}"
