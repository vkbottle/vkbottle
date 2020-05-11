# Generated with love
from .access import APIAccessibility
from .method import BaseMethod


class AppwidgetsUpdate(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.GROUP]

    async def __call__(self, code: str, type: str) -> dict:
        """ appWidgets.update
        From Vk Docs: Allows to update community app widget
        Access from group token(s)
        :param code: 
        :param type: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request("appWidgets.update", params)


class Appwidgets:
    def __init__(self, request):
        self.update = AppwidgetsUpdate(request)
