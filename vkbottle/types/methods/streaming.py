# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class StreamingGetServerUrl(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self,):
        """ streaming.getServerUrl
        From Vk Docs: Allows to receive data for the connection to Streaming API.
        Access from user, service token(s)
        
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("streaming.getServerUrl", params)


class StreamingSetSettings(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, monthly_tier: str):
        """ streaming.setSettings
        From Vk Docs: 
        Access from user, service token(s)
        :param monthly_tier: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("streaming.setSettings", params)


class Streaming:
    def __init__(self, request):
        self.get_server_url = StreamingGetServerUrl(request)
        self.set_settings = StreamingSetSettings(request)
