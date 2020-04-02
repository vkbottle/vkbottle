# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class WidgetsGetComments(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        widget_api_id: int,
        url: str,
        page_id: str,
        order: str,
        fields: typing.List,
        offset: int,
        count: int,
    ):
        """ widgets.getComments
        From Vk Docs: Gets a list of comments for the page added through the [vk.com/dev/Comments|Comments widget].
        Access from user, service token(s)
        :param widget_api_id: 
        :param url: 
        :param page_id: 
        :param order: 
        :param fields: 
        :param offset: 
        :param count: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("widgets.getComments", params)


class WidgetsGetPages(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, widget_api_id: int, order: str, period: str, offset: int, count: int
    ):
        """ widgets.getPages
        From Vk Docs: Gets a list of application/site pages where the [vk.com/dev/Comments|Comments widget] or [vk.com/dev/Like|Like widget] is installed.
        Access from user, service token(s)
        :param widget_api_id: 
        :param order: 
        :param period: 
        :param offset: 
        :param count: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("widgets.getPages", params)


class Widgets:
    def __init__(self, request):
        self.get_comments = WidgetsGetComments(request)
        self.get_pages = WidgetsGetPages(request)
