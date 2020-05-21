# Generated with love
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class StatusGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, group_id: int = None
    ) -> responses.status.Get:
        """ status.get
        From Vk Docs: Returns data required to show the status of a user or community.
        Access from user token(s)
        :param user_id: User ID or community ID. Use a negative value to designate a community ID.
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "status.get", params, response_model=responses.status.GetModel
        )


class StatusSet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, text: str = None, group_id: int = None, audio: str = None
    ) -> responses.ok_response.OkResponse:
        """ status.set
        From Vk Docs: Sets a new status for the current user.
        Access from user token(s)
        :param text: Text of the new status.
        :param group_id: Identifier of a community to set a status in. If left blank the status is set to current user.
        :param audio: needed to make status with audio
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "status.set", params, response_model=responses.ok_response.OkResponseModel
        )


class Status:
    def __init__(self, request):
        self.get = StatusGet(request)
        self.set = StatusSet(request)
