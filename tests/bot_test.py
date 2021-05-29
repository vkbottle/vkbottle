import enum
import json
import typing

import pytest
import vbml

from vkbottle import API, AndFilter, Bot, GroupEventType, GroupTypes, OrFilter, StatePeer
from vkbottle.bot import BotLabeler, Message, rules
from vkbottle.tools.dev_tools.mini_types.bot import message_min
from vkbottle.tools.test_utils import MockedClient, with_mocked_api

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
                "message": {"id": 100, "from_id": 1},
            },
        },
    ],
}


class MockIntEnum(enum.IntEnum):
    MOCK = 1


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
            return json.dumps({"response": {**data, **{"r": 1}}})

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
        assert await message.answer() == {"peer_id": message.peer_id, "r": 1}
        assert await message.answer(some_unsigned_param="test") == {
            "peer_id": message.peer_id,
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


def fake_message(ctx_api: API, **data: typing.Any) -> Message:
    return message_min(
        {
            "object": {
                "message": data,
                "client_info": data.get(
                    "client_info", EXAMPLE_EVENT["updates"][1]["object"]["client_info"]
                ),
            }
        },
        ctx_api,
    )


@pytest.mark.asyncio
@with_mocked_api(None)
async def test_rules(api: API):
    assert await rules.FromPeerRule(123).check(fake_message(api, peer_id=123))
    assert not await rules.FromUserRule().check(fake_message(api, from_id=-1))
    assert await rules.VBMLRule("i am in love with <whom>", vbml.Patcher()).check(
        fake_message(api, text="i am in love with you")
    ) == {"whom": "you"}
    assert await rules.FuncRule(lambda m: m.text.endswith("!")).check(
        fake_message(api, text="yes!")
    )
    assert not await rules.PeerRule(from_chat=True).check(fake_message(api, peer_id=1, from_id=1))
    assert await rules.PayloadMapRule([("a", int), ("b", str)]).check(
        fake_message(api, payload=json.dumps({"a": 1, "b": ""}))
    )
    assert await rules.PayloadMapRule([("a", int), ("b", [("c", str), ("d", dict)])]).check(
        fake_message(api, payload=json.dumps({"a": 1, "b": {"c": "", "d": {}}}))
    )
    assert await rules.PayloadMapRule({"a": int, "b": {"c": str, "d": dict}}).check(
        fake_message(api, payload=json.dumps({"a": 1, "b": {"c": "", "d": {}}}))
    )
    assert await rules.StickerRule(sticker_ids=[1, 2]).check(
        fake_message(api, attachments=[{"type": "sticker", "sticker": {"sticker_id": 2}}])
    )

    assert (
        await AndFilter(rules.FromPeerRule(123), rules.FromPeerRule([1, 123])).check(
            fake_message(api, peer_id=123)
        )
        is not False
    )
    assert (
        await OrFilter(rules.FromPeerRule(123), rules.FromPeerRule([1, 123])).check(
            fake_message(api, peer_id=1)
        )
        is not False
    )
    assert await rules.RegexRule(r"Hi .*?").check(fake_message(api, text="Hi bro")) == {
        "match": ()
    }
    assert await rules.RegexRule("Hi (.*?)$").check(fake_message(api, text="Hi bro")) == {
        "match": ("bro",)
    }
    assert not await rules.RegexRule(r"Hi .*?").check(fake_message(api, text="Hi")) == {
        "match": ()
    }
    assert rules.PayloadMapRule.transform_to_map({"a": int, "b": {"c": str, "d": dict}}) == [
        ("a", int),
        ("b", [("c", str), ("d", dict)]),
    ]
    assert await rules.CommandRule("cmd", ["!", "."], 2).check(
        fake_message(api, text="!cmd test bar")
    ) == {"args": ("test", "bar")}
    assert (
        await rules.CommandRule("cmd", ["!", "."], 2).check(fake_message(api, text="cmd test bar"))
        is False
    )

    # todo: if args are more than args_count do join excess args with last
    assert (
        await rules.CommandRule("cmd", ["!", "."], 1).check(fake_message(api, text="cmd test bar"))
        is False
    )

    assert (
        await rules.CommandRule("cmd", ["!", "."], 3).check(fake_message(api, text="cmd test bar"))
        is False
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
    assert await rules.PayloadRule({"cmd": "text"}).check(
        fake_message(api, payload='{"cmd":"text"}')
    )
    assert await rules.PayloadRule([{"cmd": "text"}, {"cmd": "ne text"}]).check(
        fake_message(api, payload='{"cmd":"text"}')
    )
    assert await rules.StateRule(state=None).check(fake_message(api))
    assert not await rules.StateRule(state=MockIntEnum.MOCK).check(fake_message(api))
    assert await rules.StateGroupRule(state_group=None).check(fake_message(api))
    sg_mock_message = fake_message(api)
    sg_mock_message.state_peer = StatePeer(peer_id=1, state=MockIntEnum.MOCK, payload={})
    assert await rules.StateGroupRule(state_group=MockIntEnum).check(sg_mock_message)
