# Example of sending and receiving an event after pressing the Callback button
# Documentation: https://dev.vk.com/api/bots/development/keyboard#Callback-кнопки
import logging
import os

from vkbottle import Callback, GroupEventType, Keyboard
from vkbottle.bot import Bot, Message, MessageEvent, rules

bot = Bot(os.environ["TOKEN"])
logging.basicConfig(level=logging.INFO)

KEYBOARD = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Показать текст", payload={"cmd": "snackbar"}))
    .row()
    .add(Callback("Дата регистрации (tool42)", payload={"cmd": "app"}))
    .row()
    .add(Callback("Закрыть", payload={"cmd": "close"}))
    .get_json()
)


@bot.on.private_message(text="/callback")
async def send_callback_button(message: Message):
    await message.answer("Лови!", keyboard=KEYBOARD)


@bot.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"cmd": "snackbar"}),
)
async def show_snackbar(event: MessageEvent):
    await event.show_snackbar("Сейчас я исчезну")


@bot.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"cmd": "app"}),
)
async def open_app(event: MessageEvent):
    await event.open_app(6798836, "reg", event.user_id)


@bot.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"cmd": "close"}),
)
async def edit_message(event: MessageEvent):
    await event.edit_message("Окей")


bot.run_forever()
