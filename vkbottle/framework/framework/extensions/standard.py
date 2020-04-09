from .extension import AbstractExtension
import random
from vkbottle.api.api.api import Api


class StandardExtension(AbstractExtension):
    def random_id(self):
        return random.randint(-2e9, 2e9)

    def api_instance(self) -> Api:
        return Api.get_current()

    def group_id(self):
        return self.api_instance().group_id
