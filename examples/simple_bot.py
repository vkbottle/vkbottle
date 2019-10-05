from vkbottle import Bot, Message, keyboard_generator, events

bot = Bot(token='token', group_id=1, debug=True)

"""Bot functions
When bot receive message «hi» in private chat it answers «hi, my lil friend« and sends a keyboard
If user joins, bot will try to send a message «Welcome to the group!»
If bot can't do it and VKError with codes 901 or 902 appeared, bot uses logger to send a log about it
"""


@bot.on.message('hi')
async def wrapper(ans: Message):
    keyboard = [[{'text': 'fantastic button'}]]
    await ans('hi, my lil friend', keyboard=keyboard_generator(keyboard))


@bot.on.event.group_join()
async def wrapper(event: events.GroupJoin):
    await bot.api.messages.send(peer_id=event.user_id, random_id=100, message='Welcome to the group!')


@bot.error_handler(901, 902)
async def error(error: list):
    await bot.logger('Cant send message to this user :(, error code:', error[0])


if __name__ == '__main__':
    bot.run_polling()
