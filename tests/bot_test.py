from vkbottle import Bot, API
from vkbottle.tools.test_utils import with_mocked_api, MockedClient
import pytest
import typing
import json

EXAMPLE_EVENT = {
    "ts": 1,
    "updates": [
        {
            "type": "wall_post_new",
            "object": {
                "id": 28,
                "from_id": -123456,
                "owner_id": -123456,
                "date": 1519631591,
                "marked_as_ads": 0,
                "post_type": "post",
                "text": "Post text",
                "can_edit": 1,
                "created_by": 564321,
                "can_delete": 1,
                "comments": {"count": 0},
            },
            "group_id": 123456,
        }
    ],
}


def set_http_callback(api: API, callback: typing.Callable[[dict], typing.Any]):
    api.http._session = MockedClient(callback=callback)


@pytest.mark.asyncio
async def test_bot_polling():
    def callback(data: dict):
        if "groups.getById" in data["url"]:
            return {"response": [{"id": 1}]}
        elif "groups.getLongPollServer" in data["url"]:
            return {"response": {"ts": 1, "server": "!SERVER!", "key": ""}}
        elif "!SERVER!" in data["url"]:
            return EXAMPLE_EVENT

    bot = Bot("token")
    set_http_callback(bot.api, callback)

    async for event in bot.polling.listen():
        assert event.get("updates")
        for update in event["updates"]:
            await bot.router.route(update, bot.api)
        break


@pytest.mark.asyncio
async def test_bot_scopes():
    bot = Bot(token="some token")
    assert bot.api.token == "some token"
    assert bot.api == bot.polling.api
    assert bot.labeler.message_view is bot.router.views["message"]
    assert bot.labeler.raw_event_view is bot.router.views["raw"]
