import pytest
import os
from vkbottle.api import API

TOKEN = os.getenv("token")

@pytest.fixture()
def api_getter():
    return API(TOKEN)
