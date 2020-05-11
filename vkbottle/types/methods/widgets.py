# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class WidgetsGetComments(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        widget_api_id: int = None,
        url: str = None,
        page_id: str = None,
        order: str = None,
        fields: typing.List = None,
        offset: int = None,
        count: int = None,
    ) -> responses.widgets.GetComments:
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

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "widgets.getComments",
            params,
            response_model=responses.widgets.GetCommentsModel,
        )


class WidgetsGetPages(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        widget_api_id: int = None,
        order: str = None,
        period: str = None,
        offset: int = None,
        count: int = None,
    ) -> responses.widgets.GetPages:
        """ widgets.getPages
        From Vk Docs: Gets a list of application/site pages where the [vk.com/dev/Comments|Comments widget] or [vk.com/dev/Like|Like widget] is installed.
        Access from user, service token(s)
        :param widget_api_id: 
        :param order: 
        :param period: 
        :param offset: 
        :param count: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "widgets.getPages", params, response_model=responses.widgets.GetPagesModel
        )


class Widgets:
    def __init__(self, request):
        self.get_comments = WidgetsGetComments(request)
        self.get_pages = WidgetsGetPages(request)
