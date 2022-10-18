import json
from typing import Any, Callable

import pytest
import vbml
from vkbottle_types.methods.base_category import BaseCategory

from vkbottle import (
    API,
    AndRule,
    BaseStateGroup,
    Bot,
    GroupEventType,
    GroupTypes,
    NotRule,
    OrRule,
    StatePeer,
)
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules import base
from vkbottle.tools.dev.mini_types.bot import message_min
from tests.test_utils import MockedClient, with_mocked_api

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
                        "callback",
                    ],
                    "keyboard": True,
                    "inline_keyboard": True,
                    "carousel": False,
                    "lang_id": 0,
                },
                "message": {
                    "id": 100,
                    "from_id": 1,
                    "peer_id": 1,
                    "date": 1,
                    "text": "test",
                    "out": 0,
                },
            },
        },
    ],
}


class FirstMockState(BaseStateGroup):
    MOCK = 1


class SecondMockState(BaseStateGroup):
    MOCK = 1


class MessagesCategory(BaseCategory):
    async def send(self, **data: Any) -> Any:
        return (await self.api.request("messages.send", data))["response"]


class GroupsCategory(BaseCategory):
    async def get_by_id(self, **data: Any) -> Any:
        return (await self.api.request("groups.getById", data))["response"]

    async def get_long_poll_server(self, **data: Any) -> Any:
        return (await self.api.request("groups.getLongPollServer", data))["response"]


def set_http_callback(api: API, callback: Callable[[str, str, dict], Any]):
    api.http_client = MockedClient(callback=callback)


async def test_bot_polling():  # noqa: CCR001
    class TestApi(API):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @property
        def groups(self):
            return GroupsCategory(self)

        @property
        def messages(self):
            return MessagesCategory(self)

    def callback(method: str, url: str, data: dict):
        if "groups.getById" in url:
            return {"response": [{"id": 1}]}
        elif "groups.getLongPollServer" in url:
            return {"response": {"ts": 1, "server": "!SERVER!", "key": ""}}
        elif "!SERVER!" in url:
            return EXAMPLE_EVENT
        elif "messages.send" in url:
            _r = {**data, "r": 1}
            return {"response": [_r]} if "peer_ids" in data else {"response": _r}

    bot = Bot(api=TestApi("token"))
    set_http_callback(bot.api, callback)

    @bot.labeler.raw_event(GroupEventType.WALL_POST_NEW, GroupTypes.WallPostNew)
    async def wall_post_handler(post: GroupTypes.WallPostNew):
        assert post.object.owner_id == -123456
        assert post.ctx_api == bot.api

    @bot.labeler.message()
    async def message_handler(message: Message):
        assert message.id == 100
        assert message.from_id == 1
        assert await message.answer() == {
            "peer_ids": str(message.peer_id),
            "r": 1,
            "random_id": 0,
        }
        assert await message.answer(some_unsigned_param="test") == {
            "peer_ids": str(message.peer_id),
            "random_id": 0,
            "some_unsigned_param": "test",
            "r": 1,
        }

    async for event in bot.polling.listen():
        assert event.get("updates")
        for update in event["updates"]:
            await bot.router.route(update, bot.api)
        break


@pytest.mark.asyncio
async def test_bot_scopes():
    bot = Bot(token="some token")
    assert await bot.api.token_generator.get_token() == "some token"
    assert bot.api == bot.polling.api
    assert bot.labeler.message_view is bot.router.views["message"]
    assert bot.labeler.raw_event_view is bot.router.views["raw"]


def fake_message(ctx_api: API, **data: Any) -> Message:
    message = {"peer_id": 1, "date": 1, "from_id": 1, "text": "test", "out": 0, "id": 1}
    message.update(data)
    return message_min(
        {
            "object": {
                "message": message,
                "client_info": message.get(
                    "client_info", EXAMPLE_EVENT["updates"][1]["object"]["client_info"]
                ),
            }
        },
        ctx_api,
    )


@pytest.mark.asyncio
@with_mocked_api(None)
async def test_rules(api: API):
    assert await base.FromPeerRule(123).check(fake_message(api, peer_id=123))
    assert not await base.FromUserRule().check(fake_message(api, from_id=-1))
    assert await base.VBMLRule("i am in love with <whom>", vbml.Patcher()).check(
        fake_message(api, text="i am in love with you")
    ) == {"whom": "you"}
    assert await base.FuncRule(lambda m: m.text.endswith("!")).check(
        fake_message(api, text="yes!")
    )
    assert not await base.PeerRule().check(fake_message(api, peer_id=1, from_id=1))
    assert await base.PayloadMapRule([("a", int), ("b", str)]).check(
        fake_message(api, payload=json.dumps({"a": 1, "b": ""}))
    )
    assert await base.PayloadMapRule([("a", int), ("b", [("c", str), ("d", dict)])]).check(
        fake_message(api, payload=json.dumps({"a": 1, "b": {"c": "", "d": {}}}))
    )
    assert await base.PayloadMapRule({"a": int, "b": {"c": str, "d": dict}}).check(
        fake_message(api, payload=json.dumps({"a": 1, "b": {"c": "", "d": {}}}))
    )
    assert await base.StickerRule(sticker_ids=[1, 2]).check(
        fake_message(api, attachments=[{"type": "sticker", "sticker": {"sticker_id": 2}}])
    )

    assert (
        await AndRule(base.FromPeerRule(123), base.FromPeerRule([1, 123])).check(
            fake_message(api, peer_id=123)
        )
        is not False
    )
    assert (
        await OrRule(base.FromPeerRule(123), base.FromPeerRule([1, 123])).check(
            fake_message(api, peer_id=1)
        )
        is not False
    )
    assert await NotRule(base.FromPeerRule(123)).check(fake_message(api, peer_id=1)) is not False
    assert await base.RegexRule(r"Hi .*?").check(fake_message(api, text="Hi bro")) == {"match": ()}
    assert await base.RegexRule("Hi (.*?)$").check(fake_message(api, text="Hi bro")) == {
        "match": ("bro",)
    }
    assert await base.RegexRule(r"Hi .*?").check(fake_message(api, text="Hi")) != {"match": ()}

    assert base.PayloadMapRule.transform_to_map({"a": int, "b": {"c": str, "d": dict}}) == [
        ("a", int),
        ("b", [("c", str), ("d", dict)]),
    ]
    assert await base.CommandRule("cmd", ["!", "."], 2).check(
        fake_message(api, text="!cmd test bar")
    ) == {"args": ["test", "bar"]}
    assert (
        await base.CommandRule("cmd", ["!", "."], 2).check(fake_message(api, text="cmd test bar"))
        is False
    )

    # todo: if args are more than args_count do join excess args with last
    assert (
        await base.CommandRule("cmd", ["!", "."], 1).check(fake_message(api, text="cmd test bar"))
        is False
    )

    assert (
        await base.CommandRule("cmd", ["!", "."], 3).check(fake_message(api, text="cmd test bar"))
        is False
    )

    assert (
        await base.CommandRule("cmd", ["!", "."], 0).check(fake_message(api, text="!cmd test bar"))
        is False
    )

    assert (
        await base.CommandRule("cmd", ["!", "."], 0).check(fake_message(api, text="!cmd")) is True
    )

    labeler = BotLabeler()
    labeler.vbml_ignore_case = True
    assert (
        await labeler.get_custom_rules({"text": "privet"})[0].check(
            fake_message(api, text="Privet")
        )
        == {}
    )
    labeler.vbml_ignore_case = False
    assert not await labeler.get_custom_rules({"text": "privet"})[0].check(
        fake_message(api, text="Private")
    )
    assert await base.PayloadRule({"cmd": "text"}).check(
        fake_message(api, payload='{"cmd":"text"}')
    )
    assert await base.PayloadRule([{"cmd": "text"}, {"cmd": "ne text"}]).check(
        fake_message(api, payload='{"cmd":"text"}')
    )
    s_mock_message = fake_message(api)
    s_mock_message.state_peer = StatePeer(peer_id=1, state=FirstMockState.MOCK)
    assert await base.StateRule(state=FirstMockState.MOCK).check(s_mock_message)
    assert not await base.StateRule(state=SecondMockState.MOCK).check(s_mock_message)
    assert await base.StateRule(state=None).check(fake_message(api))
    assert await base.StateGroupRule(state_group=None).check(fake_message(api))
    sg_mock_message = fake_message(api)
    sg_mock_message.state_peer = StatePeer(peer_id=1, state=FirstMockState.MOCK, payload={})
    assert await base.StateGroupRule(state_group=FirstMockState).check(sg_mock_message)
    assert not await base.StateGroupRule(state_group=SecondMockState).check(sg_mock_message)
