from vkbottle.tools import (
    Keyboard,
    KeyboardButtonColor,
    Text,
    Callback,
    CtxStorage,
    LoopWrapper,
    template_gen,
    TemplateElement,
)
from vkbottle.modules import json

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


class MockedLoop:
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


def test_loop_wrapper():
    async def task1():
        pass

    async def task2():
        pass

    async def task3():
        pass

    lw = LoopWrapper(tasks=[task1])
    lw.on_startup.append(task2)
    lw.on_shutdown.append(task3)

    lw.run_forever(MockedLoop())

    assert ctx_storage.get("checked-test-lw-create-task") == task1.__name__
    assert ctx_storage.get("checked-test-lw-run-until-complete") == [
        task2.__name__,
        task3.__name__,
    ]
    assert ctx_storage.get("checked-test-lw-run-forever")
