from __future__ import annotations

import asyncio
import os
import re
from io import StringIO
from typing import TYPE_CHECKING

import pytest

from vkbottle import API
from vkbottle.bot import Bot, run_multibot
from vkbottle.dispatch import ABCRule, AndRule, NotRule, OrRule
from vkbottle.exception_factory.base_exceptions import APIAuthError, VKAPIError
from vkbottle.modules import json
from vkbottle.tools import (
    CallableValidator,
    Callback,
    CtxStorage,
    EqualsValidator,
    IsInstanceValidator,
    Keyboard,
    KeyboardButtonColor,
    LoopWrapper,
    TemplateElement,
    Text,
    UserAuth,
    load_blueprints_from_package,
    run_in_task,
    template_gen,
)

if TYPE_CHECKING:
    from aioresponses import aioresponses
    from pytest_mock import MockerFixture

KEYBOARD_JSON = json.dumps(
    {
        "one_time": True,
        "inline": False,
        "buttons": [
            [
                {
                    "action": {
                        "label": "I love nuggets",
                        "payload": {"love": "nuggets"},
                        "type": "text",
                    }
                }
            ],
            [
                {
                    "action": {
                        "label": "Eat nuggets",
                        "payload": {"eat": "nuggets"},
                        "type": "callback",
                    },
                    "color": "positive",
                }
            ],
        ],
    }
)

TEMPLATE_DICT = {
    "type": "carousel",
    "elements": [
        {
            "photo_id": "-109837093_457242811",
            "action": {"type": "open_photo"},
            "buttons": [{"action": {"type": "text", "label": "text", "payload": "{}"}}],
        },
        {
            "photo_id": "-109837093_457242811",
            "action": {"type": "open_photo"},
            "buttons": [{"action": {"type": "text", "label": "text 2", "payload": "{}"}}],
        },
    ],
}

ctx_storage = CtxStorage()


def assert_rule(res, rev=False):
    assert (res is not False) is not rev


def test_keyboard_non_builder():
    keyboard = Keyboard(one_time=True)
    keyboard.row()  # test empty row autoremove
    keyboard.add(Text("I love nuggets", {"love": "nuggets"}))
    keyboard.row()
    keyboard.add(Callback("Eat nuggets", {"eat": "nuggets"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()  # test empty row autoremove
    assert keyboard.get_json() == KEYBOARD_JSON


def test_keyboard_builder():
    assert (
        Keyboard(one_time=True)
        .add(Text("I love nuggets", {"love": "nuggets"}))
        .row()
        .add(Callback("Eat nuggets", {"eat": "nuggets"}), color=KeyboardButtonColor.POSITIVE)
        .get_json()
    ) == KEYBOARD_JSON


def test_bp_importer(mocker: "MockerFixture"):
    required_files = ["bp1.py", "bp2.py", "bp3.py", "bp4.py"]
    main_package = os.path.join("src", "folder")
    main_files = {
        os.path.join(main_package, "bp1.py"): "bp = Blueprint('blup')",
        os.path.join(main_package, "bp2.py"): "\n#\nbp = Blueprint('blup2')",
        os.path.join(
            main_package, "__init__.py"
        ): "from . import bp1, bp2\nfrom .bps import bp3, bp4",
    }
    bps_files = {
        os.path.join(main_package, "bps", "bp3.py"): "blueprint = Blueprint('blup')",
        os.path.join(main_package, "bps", "bp4.py"): "bp = BotBlueprint()",
    }
    mocker.patch(
        "os.listdir",
        lambda f: (
            ["bp1.py", "__init__.py", "bp2.py", "bps"]
            if "bps" not in f
            else ["bp3.py", "bp4.py", "__init__.py"]
        ),
    )
    mocker.patch(
        "builtins.open",
        lambda fln, encoding: StringIO((main_files if "bps" not in fln else bps_files)[fln]),
    )
    mocker.patch(
        "importlib.import_module",
        lambda pn: type("A", (object,), {"__getattr__": lambda x, y: pn})(),
    )

    for bp in load_blueprints_from_package(main_package):
        required_files.pop(required_files.index(f'{str(bp).split(".")[-1]}.py'))

    assert not required_files


def test_template_generator():
    assert (
        json.loads(
            template_gen(
                TemplateElement(
                    photo_id="-109837093_457242811",
                    action={"type": "open_photo"},
                    buttons=[{"action": {"type": "text", "label": "text", "payload": "{}"}}],
                ),
                TemplateElement(
                    photo_id="-109837093_457242811",
                    action={"type": "open_photo"},
                    buttons=[{"action": {"type": "text", "label": "text 2", "payload": "{}"}}],
                ),
            )
        )
        == TEMPLATE_DICT
    )


@pytest.mark.asyncio
async def test_validators():
    assert await IsInstanceValidator((int, str)).check("foo")
    assert not await EqualsValidator("foo").check("bar")
    assert await CallableValidator(lambda _: True).check(0)


def test_loop_wrapper():
    async def task1():
        ctx_storage.set("checked-test-lw-create-task", "task1")

    async def task2():
        c = ctx_storage.get("checked-test-lw-run-until-complete") or []
        ctx_storage.set("checked-test-lw-run-until-complete", [*c, "task2"])

    async def task3():
        c = ctx_storage.get("checked-test-lw-run-until-complete") or []
        ctx_storage.set("checked-test-lw-run-until-complete", [*c, "task3"])

    lw = LoopWrapper(tasks=[task1()])
    lw.on_startup.append(task2())
    lw.on_shutdown.append(task3())

    lw.run()  # type: ignore

    assert ctx_storage.get("checked-test-lw-create-task") == task1.__name__
    assert ctx_storage.get("checked-test-lw-run-until-complete") == [
        task2.__name__,
        task3.__name__,
    ]


@pytest.mark.asyncio
async def test_utils(mocker: "MockerFixture"):
    async def task_to_run(s, y):
        ctx_storage.set("checked-test-lw-create-task", "task_to_run")
        return s.x == y

    a = type("A", (object,), {"x": 1})
    task = run_in_task(task_to_run(a, 1))
    await asyncio.gather(task)

    assert ctx_storage.get("checked-test-lw-create-task") == "task_to_run"

    c_rule = type(
        "c_rule", (ABCRule,), {"check": task_to_run, "__init__": lambda s, i: setattr(s, "x", i)}
    )

    assert (c_rule(None) | c_rule(None)).__class__ == OrRule(c_rule(None)).__class__  # type: ignore
    assert (c_rule(None) & c_rule(None)).__class__ == AndRule(c_rule(None)).__class__  # type: ignore
    assert (~c_rule(None)).__class__ == NotRule(c_rule(None)).__class__  # type: ignore

    assert_rule(await (c_rule(1) | c_rule(2)).check(2))  # type: ignore
    assert_rule(await (c_rule(1) | c_rule(2)).check(4), True)  # type: ignore
    assert_rule(await (c_rule(4) & c_rule(4)).check(4))  # type: ignore
    assert_rule(await (c_rule(2) & c_rule(4)).check(4), True)  # type: ignore
    assert_rule(await (~c_rule(1)).check(2))  # type: ignore
    assert_rule(await (~c_rule(2)).check(2), True)  # type: ignore


def test_run_multibot(mocker: "MockerFixture"):
    bot_apis = []

    mocker.patch("vkbottle.bot.Bot.run_polling", lambda s, custom_polling: s.api)
    mocker.patch("asyncio.iscoroutine", return_value=True)
    mocker.patch(
        "vkbottle.tools.loop_wrapper.LoopWrapper.run",
        lambda s: bot_apis.extend(s.tasks),
    )

    run_multibot(Bot(), (API("1"), API("2"), API("3")))
    assert len(bot_apis) == 3  # type: ignore


@pytest.mark.asyncio
async def test_user_auth(mock_aioresponse: aioresponses):
    mock_aioresponse.post(
        "https://oauth.vk.com/token",
        payload={"access_token": "token"},
    )

    token = await UserAuth(client_id=1234, client_secret="secret").get_token("login", "password")

    assert token == "token"  # noqa: S105


@pytest.mark.parametrize("validation_type", ["2fa_app", "2fa_sms"])
@pytest.mark.asyncio
async def test_user_auth_with_2fa(mock_aioresponse: aioresponses, validation_type: str):
    mock_aioresponse.post(
        "https://oauth.vk.com/token",
        payload={
            "error": "need_validation",
            "error_description": "open redirect_uri in browser [5]. Also you can use 2fa_supported param",
            "validation_type": validation_type,
            "validation_sid": "2fa_123456789_1234567_4h45c0f3a79c8kb78e",
            "phone_mask": "+7 *** *** ** 89",
            "redirect_uri": "https://m.vk.com/login?act=authcheck&api_hash=someapihash",
        },
    )

    with pytest.raises(APIAuthError) as exc_info:
        await UserAuth(client_id=1234, client_secret="secret").get_token("login", "password")

    assert exc_info.value.validation_type == validation_type
    assert exc_info.value.validation_sid == "2fa_123456789_1234567_4h45c0f3a79c8kb78e"
    assert exc_info.value.phone_mask == "+7 *** *** ** 89"
    assert (
        exc_info.value.redirect_uri == "https://m.vk.com/login?act=authcheck&api_hash=someapihash"
    )


@pytest.mark.asyncio
async def test_validate_phone(mock_aioresponse: aioresponses):
    expected_response = {
        "response": {
            "type": "general",
            "sid": "2fa_123456789_1234567_4h45c0f3a32c8kb78e",
            "delay": 60,
            "libverify_support": False,
            "validation_type": "sms",
            "validation_resend": "sms",
            "code_length": 6,
        }
    }
    mock_aioresponse.get(
        re.compile(r"^https://api\.vk\.com/method/auth\.validatePhone.*$"),
        payload=expected_response,
    )

    response = await UserAuth().validate_phone(
        validation_sid="2fa_123456789_1234567_4h45c0f3a32c8kb78e"
    )

    assert response == expected_response


@pytest.mark.asyncio
async def test_validate_phone_with_invalid_sid(mock_aioresponse: aioresponses):
    mock_aioresponse.get(
        re.compile(r"^https://api\.vk\.com/method/auth\.validatePhone.*$"),
        payload={
            "error": {
                "error_code": 100,
                "error_msg": "One of the parameters specified was missing or invalid: sid is wrong",
                "request_params": [
                    {"key": "sid", "value": "invalid_sid"},
                    {"key": "lang", "value": "en"},
                    {"key": "v", "value": "5.199"},
                    {"key": "method", "value": "auth.validatePhone"},
                    {"key": "oauth", "value": "1"},
                ],
            }
        },
    )

    with pytest.raises(VKAPIError[100]) as exc_info:
        await UserAuth().validate_phone(validation_sid="invalid_sid")

    assert (
        exc_info.value.error_msg
        == "One of the parameters specified was missing or invalid: sid is wrong"
    )
