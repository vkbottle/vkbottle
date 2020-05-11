# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class SearchGetHints(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        q: str = None,
        offset: int = None,
        limit: int = None,
        filters: typing.List = None,
        fields: typing.List = None,
        search_global: bool = None,
    ) -> responses.search.GetHints:
        """ search.getHints
        From Vk Docs: Allows the programmer to do a quick search for any substring.
        Access from user token(s)
        :param q: Search query string.
        :param offset: Offset for querying specific result subset
        :param limit: Maximum number of results to return.
        :param filters: 
        :param fields: 
        :param search_global: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "search.getHints", params, response_model=responses.search.GetHintsModel
        )


class Search:
    def __init__(self, request):
        self.get_hints = SearchGetHints(request)
