# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class StorageGet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, key: str, keys: typing.List, user_id: int):
        """ storage.get
        From Vk Docs: Returns a value of variable with the name set by key parameter.
        Access from user token(s)
        :param key: 
        :param keys: 
        :param user_id: 
        :param global: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("storage.get", params)


class StorageGetKeys(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_id: int, offset: int, count: int):
        """ storage.getKeys
        From Vk Docs: Returns the names of all variables.
        Access from user token(s)
        :param user_id: user id, whose variables names are returned if they were requested with a server method.
        :param global: 
        :param offset: 
        :param count: amount of variable names the info needs to be collected from.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("storage.getKeys", params)


class StorageSet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, key: str, value: str, user_id: int):
        """ storage.set
        From Vk Docs: Saves a value of variable with the name set by 'key' parameter.
        Access from user token(s)
        :param key: 
        :param value: 
        :param user_id: 
        :param global: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("storage.set", params)


class Storage:
    def __init__(self, request):
        self.get = StorageGet(request)
        self.get_keys = StorageGetKeys(request)
        self.set = StorageSet(request)
