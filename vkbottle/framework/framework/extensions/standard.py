from .extension import AbstractExtension
from .storage import CtxStorage
import random
from vkbottle.api.api.api import get_api, API


class StandardExtension(AbstractExtension):
    def random_id(self):
        return random.randint(-2e9, 2e9)

    def api_instance(self) -> API:
        return get_api()

    def group_id(self):
        return self.api_instance().group_id

    @property
    def storage(self) -> CtxStorage:
        return CtxStorage()
