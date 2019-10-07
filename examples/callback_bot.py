from vkbottle import Message, Bot, keyboard_gen
from flask import request, Flask
import sys

app = Flask(__name__)
bot = Bot(token=open('token').readline(),
          group_id=1,
          debug=True,)
confirmation = 'MyConfirmation'

keyboard = keyboard_gen(
[
    [
        {'text': 'do $ex'},
        {'text': 'make me con', 'color': 'negative'}
    ],
    [
        {'text': 'cry..'}
    ]
],
    one_time=True)


@app.route('/bot')
def route():
    event = request.get_json(force=True, silent=True)
    return bot.process(event, confirmation_token=confirmation)


@bot.on.message_both.lower('hi <name>')
async def wrapper(ans: Message, name):
    await ans(f'i\'m not a {name}', keyboard=keyboard)
