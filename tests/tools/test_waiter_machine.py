import asyncio

from tests.test_bot import fake_message
from tests.test_utils import with_mocked_api
from vkbottle.bot import rules
from vkbottle.dispatch.views.bot.message import BotMessageView
from vkbottle.tools import WaiterMachine


async def send_events(wm, api, view) -> None:
    await view.handle_event(
        {
            "type": "message_new",
            "object": {
                "message": fake_message(api, peer_id=11, text="123").__dict__,
            },
        },
        api,
        wm.middleware.state_dispenser,
    )
    await view.handle_event(
        {
            "type": "message_new",
            "object": {
                "message": fake_message(api, peer_id=12, text="12345").__dict__,
            },
        },
        api,
        wm.middleware.state_dispenser,
    )
    await view.handle_event(
        {
            "type": "message_new",
            "object": {
                "message": fake_message(api, peer_id=11, text="12345").__dict__,
            },
        },
        api,
        wm.middleware.state_dispenser,
    )


@with_mocked_api(None)
async def test_waiter_machine(api) -> None:
    wm = WaiterMachine()
    view = BotMessageView()

    msg = fake_message(api, peer_id=11, text="123")

    tasks = [
        wm.wait(view, msg, rules.MessageLengthRule(5)),
        send_events(wm, api, view),
    ]

    (msg, ctx), _ = await asyncio.gather(*tasks)
    assert ctx == {}
    assert msg.peer_id == 11
    assert msg.text == "12345"
