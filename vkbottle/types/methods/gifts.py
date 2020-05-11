# Generated with love
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class GiftsGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, count: int = None, offset: int = None
    ) -> responses.gifts.Get:
        """ gifts.get
        From Vk Docs: Returns a list of user gifts.
        Access from user token(s)
        :param user_id: User ID.
        :param count: Number of gifts to return.
        :param offset: Offset needed to return a specific subset of results.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "gifts.get", params, response_model=responses.gifts.GetModel
        )


class Gifts:
    def __init__(self, request):
        self.get = GiftsGet(request)
