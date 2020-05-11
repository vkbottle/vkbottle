# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class StorageGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        key: str = None,
        keys: typing.List = None,
        user_id: int = None,
        global_: bool = None,
    ) -> responses.storage.Get:
        """ storage.get
        From Vk Docs: Returns a value of variable with the name set by key parameter.
        Access from user token(s)
        :param key: 
        :param keys: 
        :param user_id: 
        :param global: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "storage.get", params, response_model=responses.storage.GetModel
        )


class StorageGetKeys(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        user_id: int = None,
        global_: bool = None,
        offset: int = None,
        count: int = None,
    ) -> responses.storage.GetKeys:
        """ storage.getKeys
        From Vk Docs: Returns the names of all variables.
        Access from user token(s)
        :param user_id: user id, whose variables names are returned if they were requested with a server method.
        :param global: 
        :param offset: 
        :param count: amount of variable names the info needs to be collected from.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "storage.getKeys", params, response_model=responses.storage.GetKeysModel
        )


class StorageSet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, key: str, value: str = None, user_id: int = None, global_: bool = None
    ) -> responses.ok_response.OkResponse:
        """ storage.set
        From Vk Docs: Saves a value of variable with the name set by 'key' parameter.
        Access from user token(s)
        :param key: 
        :param value: 
        :param user_id: 
        :param global: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "storage.set", params, response_model=responses.ok_response.OkResponseModel
        )


class Storage:
    def __init__(self, request):
        self.get = StorageGet(request)
        self.get_keys = StorageGetKeys(request)
        self.set = StorageSet(request)
