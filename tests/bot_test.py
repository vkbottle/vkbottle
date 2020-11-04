from vkbottle import Bot, API, GroupTypes, GroupEventType
from vkbottle.bot import Message
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
        },
        {
            "type": "message_new",
            "object": {
                "client_info": {
                    "button_actions": [
                        "text",
                        "vkpay",
                        "open_app",
                        "location",
                        "open_link",
                        "callback"
                    ],
                    "keyboard": True,
                    "inline_keyboard": True,
                    "carousel": False,
                    "lang_id": 0
                },
                "message": {
                    "id": 100,
                    "from_id": 1,
                }
            }
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
        elif "messages.send" in data["url"]:
            return json.dumps({"response": 100})

    bot = Bot("token")
    set_http_callback(bot.api, callback)

    @bot.labeler.raw_event(GroupEventType.WALL_POST_NEW, GroupTypes.WallPostNew)
    async def wall_post_handler(post: GroupTypes.WallPostNew):
        assert post.object.owner_id == -123456
        assert post.ctx_api == bot.api

    @bot.labeler.message()
    async def message_handler(message: Message):
        assert message.id == 100
        assert message.from_id == 1
        assert await message.answer() == 100

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
