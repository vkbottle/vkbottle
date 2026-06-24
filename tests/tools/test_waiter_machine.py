import asyncio

from tests.test_bot import fake_message
from tests.test_utils import with_mocked_api
from vkbottle.bot import BotLabeler, rules
from vkbottle.dispatch.dispenser.builtin import BuiltinStateDispenser
from vkbottle.dispatch.views.bot.message import BotMessageView
from vkbottle.tools import WaiterMachine


async def send_events(wm, api, view, state_dispenser) -> None:
    await view.handle_event(
        {
            "type": "message_new",
            "object": {
                "message": fake_message(api, peer_id=11, text="123").__dict__,
            },
        },
        api,
        state_dispenser,
    )
    await view.handle_event(
        {
            "type": "message_new",
            "object": {
                "message": fake_message(api, peer_id=12, text="12345").__dict__,
            },
        },
        api,
        state_dispenser,
    )
    await view.handle_event(
        {
            "type": "message_new",
            "object": {
                "message": fake_message(api, peer_id=11, text="12345").__dict__,
            },
        },
        api,
        state_dispenser,
    )


@with_mocked_api(None)
async def test_waiter_machine(api) -> None:
    wm = WaiterMachine()
    view = BotMessageView()
    state_dispenser = BuiltinStateDispenser()

    msg = fake_message(api, peer_id=11, text="123")

    tasks = [
        wm.wait(view, msg, rules.MessageLengthRule(5)),
        send_events(wm, api, view, state_dispenser),
    ]

    (msg, ctx), _ = await asyncio.gather(*tasks)
    assert ctx == {}
    assert msg.peer_id == 11
    assert msg.text == "12345"


@with_mocked_api(None)
async def test_waiter_machine_with_loaded_labeler(api) -> None:
    host = BotLabeler()
    child = BotLabeler()

    host.load(child)

    state_dispenser = BuiltinStateDispenser()

    wm = WaiterMachine()
    trigger = fake_message(api, peer_id=11, text="/test")

    async def deliver_next() -> None:
        await asyncio.sleep(0)
        await host.message_view.handle_event(
            {
                "type": "message_new",
                "object": {
                    "message": fake_message(api, peer_id=11, text="reply").__dict__,
                },
            },
            api,
            state_dispenser,
        )

    wait_task = asyncio.create_task(wm.wait(child.message_view, trigger))
    deliver_task = asyncio.create_task(deliver_next())

    msg, ctx = await asyncio.wait_for(wait_task, timeout=1.0)
    await deliver_task

    assert ctx == {}
    assert msg.peer_id == 11
    assert msg.text == "reply"
