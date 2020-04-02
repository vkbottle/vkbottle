# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class StatusGet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_id: int, group_id: int):
        """ status.get
        From Vk Docs: Returns data required to show the status of a user or community.
        Access from user token(s)
        :param user_id: User ID or community ID. Use a negative value to designate a community ID.
        :param group_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("status.get", params)


class StatusSet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, text: str, group_id: int):
        """ status.set
        From Vk Docs: Sets a new status for the current user.
        Access from user token(s)
        :param text: Text of the new status.
        :param group_id: Identifier of a community to set a status in. If left blank the status is set to current user.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("status.set", params)


class Status:
    def __init__(self, request):
        self.get = StatusGet(request)
        self.set = StatusSet(request)
