import os
from io import StringIO

import pytest
from pytest_mock import MockerFixture

from vkbottle import API
from vkbottle.bot import Bot, run_multibot
from vkbottle.dispatch import ABCRule, AndRule, NotRule, OrRule
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
    keyboard_gen,
    load_blueprints_from_package,
    run_in_task,
    template_gen,
)

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


class MockedLoop:  # noqa: PIE798
    @staticmethod
    def create_task(task):
        ctx_storage.set("checked-test-lw-create-task", task.__name__)

    @staticmethod
    def run_until_complete(task):
        c = ctx_storage.get("checked-test-lw-run-until-complete") or []
        ctx_storage.set("checked-test-lw-run-until-complete", [*c, task.__name__])

    @staticmethod
    def run_forever():
        ctx_storage.set("checked-test-lw-run-forever", True)

    @staticmethod
    def is_running():
        return False


def test_keyboard_non_builder():
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("I love nuggets", {"love": "nuggets"}))
    keyboard.row()
    keyboard.add(Callback("Eat nuggets", {"eat": "nuggets"}), color=KeyboardButtonColor.POSITIVE)
    assert keyboard.get_json() == KEYBOARD_JSON


def test_keyboard_builder():
    assert (
        Keyboard(one_time=True)
        .add(Text("I love nuggets", {"love": "nuggets"}))
        .row()
        .add(Callback("Eat nuggets", {"eat": "nuggets"}), color=KeyboardButtonColor.POSITIVE)
        .get_json()
    ) == KEYBOARD_JSON


def test_keyboard_generator():
    with pytest.deprecated_call():
        assert json.loads(
            keyboard_gen(
                [
                    [{"label": "I love nuggets", "payload": {"love": "nuggets"}}],
                    [
                        {
                            "type": "callback",
                            "label": "Eat nuggets",
                            "payload": {"eat": "nuggets"},
                            "color": "positive",
                        }
                    ],
                ],
                one_time=True,
            )
        ) == json.loads(KEYBOARD_JSON)


def test_bp_importer(mocker: MockerFixture):
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
        lambda f: ["bp1.py", "__init__.py", "bp2.py", "bps"]
        if "bps" not in f
        else ["bp3.py", "bp4.py", "__init__.py"],
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

    assert not len(required_files)


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
        pass

    async def task2():
        pass

    async def task3():
        pass

    lw = LoopWrapper(tasks=[task1])  # type: ignore
    lw.on_startup.append(task2)  # type: ignore
    lw.on_shutdown.append(task3)  # type: ignore

    lw.run_forever(MockedLoop())  # type: ignore

    assert ctx_storage.get("checked-test-lw-create-task") == task1.__name__
    assert ctx_storage.get("checked-test-lw-run-until-complete") == [
        task2.__name__,
        task3.__name__,
    ]
    assert ctx_storage.get("checked-test-lw-run-forever")


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore:coroutine")
async def test_utils(mocker: MockerFixture):
    async def task_to_run(s, y: int):
        return s.x == y

    mocker.patch("asyncio.get_running_loop", lambda: MockedLoop())
    run_in_task(task_to_run(1, 1))

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


def test_run_multibot(mocker: MockerFixture):
    bot_apis = []

    mocker.patch("vkbottle.bot.Bot.run_polling", lambda s, custom_polling: s.api)
    mocker.patch("asyncio.iscoroutine", lambda _: True)
    mocker.patch(
        "vkbottle.tools.dev.loop_wrapper.LoopWrapper.run_forever",
        lambda s: bot_apis.extend(s.tasks),
    )

    run_multibot(Bot(), (API("1"), API("2"), API("3")))
    assert len(bot_apis) == 3  # type: ignore
