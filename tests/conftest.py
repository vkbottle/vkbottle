import pytest
import os
from vkbottle.api import API

TOKEN = os.getenv("TOKEN")


@pytest.fixture()
def api():
    return API(TOKEN)
