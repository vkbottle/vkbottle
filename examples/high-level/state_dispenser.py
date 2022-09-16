import os

from vkbottle import BaseStateGroup, Keyboard, Text
from vkbottle.bot import Bot, Message

# Create a simple bot
bot = Bot(os.environ["token"])

# StateDispenser can be accessed / set with
# bot.state_dispenser


# Let's make a group of states
# State group is IntEnum
class MenuState(BaseStateGroup):
    START = 1
    INFO = 2


# <state = None> handles all events with no state;
# you can add StateRule to auto_rules in blueprint for example
@bot.on.private_message(state=None)
async def start_handler(message: Message):
    await message.answer(
        "Hi! Welcome to the start menu, use menu buttons",
        keyboard=(
            Keyboard()
            .add(Text("Info", {"cmd": "info"}))
            .add(Text("Buy coffee", {"cmd": "buy"}))
            .get_json()
        ),
    )
    # If you handle chats you can set state dispenser key to from_id
    # or you can implement custom state dispenser and base on other features
    await bot.state_dispenser.set(message.peer_id, MenuState.START)


@bot.on.private_message(state=MenuState.START, payload={"cmd": "info"})
async def info_handler(message: Message):
    await message.answer(
        "What are you interested in?",
        keyboard=(
            Keyboard()
            .add(Text("Books", {"item": "books"}))
            .add(Text("Cinema", {"item": "cinema"}))
            .add(Text("Undo", {"item": "undo"}))
            .get_json()
        ),
    )
    await bot.state_dispenser.set(message.peer_id, MenuState.INFO)


@bot.on.private_message(state=MenuState.INFO, payload_map=[("item", str)])
async def info_item_handler(message: Message):
    payload: dict = message.get_payload_json()  # type: ignore
    await message.answer(f"Cool! I am too interested in {payload['item']}!")
    await start_handler(message)


@bot.on.private_message(state=MenuState.START, payload={"cmd": "buy"})
async def buy_handler(_):
    return "Ok buy it here: https://example.com"


bot.run_forever()
