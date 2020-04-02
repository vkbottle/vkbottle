# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class GiftsGet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_id: int, count: int, offset: int):
        """ gifts.get
        From Vk Docs: Returns a list of user gifts.
        Access from user token(s)
        :param user_id: User ID.
        :param count: Number of gifts to return.
        :param offset: Offset needed to return a specific subset of results.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("gifts.get", params)


class Gifts:
    def __init__(self, request):
        self.get = GiftsGet(request)
