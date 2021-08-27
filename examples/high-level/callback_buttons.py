# Example of sending and receiving an event after pressing the Callback button
# Documentation: https://vk.cc/aC9JG2

import logging
import os

from vkbottle import Callback, GroupEventType, GroupTypes, Keyboard, ShowSnackbar
from vkbottle.bot import Bot, Message

bot = Bot(os.environ["TOKEN"])
logging.basicConfig(level=logging.INFO)

KEYBOARD = (
    Keyboard(one_time=False)
    .add(Callback("Callback-кнопка", payload={"cmd": "callback"}))
    .get_json()
)


@bot.on.private_message(text="/callback")
async def send_callback_button(message: Message):
    await message.answer("Лови!", keyboard=KEYBOARD)


@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def handle_message_event(event: GroupTypes.MessageEvent):
    # event_data parameter accepts three object types
    # "show_snackbar" type

    await bot.api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=ShowSnackbar("Сейчас я исчезну").get_json(),
    )


bot.run_forever()
