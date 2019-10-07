from vkbottle import Bot, Message
bot = Bot(token='token', group_id=1, debug=True)

"""Bot functions
Described in code comments
"""

# STANDART HANDLERS


@bot.on.message('hi')
async def wrapper(ans: Message):
    # Works if message 'hi' in private dialog is received
    await ans('hi')


@bot.on.chat_message('banana')
async def wrapper(ans: Message):
    # Works if message 'banana' in chat received
    await ans('clean me..')


@bot.on.message_both('apple')
async def wrapper(ans: Message):
    # Works if message 'apple' in both (chat or private) dialog received
    await ans('steve jobs..((((')


@bot.on.chat_message.startswith('/start')
async def wrapper(ans: Message):
    # Works if message in chat starts with '/start'
    await ans('this message starts with /start, yes?')


@bot.on.message_both.regex('.*?sad.*?')
async def wrapper(ans: Message):
    # Works if regex match r'.*?sad.*?' is True
    await ans('sadness, im sad, sadistic. its all in my own!')


# EVENT HANDLER

"""
To recognise types, import events object from vkbottle
You can make type-hints to work with it easier
Like this:
"""
from vkbottle.vkbottle import events


@bot.on.event.group_join()
async def wrapper(event: events.GroupJoin):
    print('User id{} just joined the group'.format(event.user_id))


@bot.on.chat_action('chat_title_update')
async def wrapper(ans: Message):
    await ans('New chat name: {}'.format(ans.action.text))


# REGEX ARGS USE


@bot.on.message('my name is <name>')
async def wrapper(ans: Message, name):
    await ans('your name is {}'.format(name))

"""
Do not do it like this:
@bot.on.message('<arg1><arg2>')
Arguments in these instances are not separable!
"""


@bot.on.message('+<country_code>(<state_code>)<number>')
async def wrapper(ans: Message, country_code, state_code, number):
    # +0(123)456
    if country_code.isdigit() and state_code.isdigit() and number.isdigit():
        await ans('Number inputted correctly!')
    else:
        await ans('Number has been inputted incorrectly!')


# OPTIONAL HANDLERS


@bot.error_handler(1, 3, 5)
async def error_wrapper(error):
    print('Catching VKError with code 1, 3 or 5', error[1])


@bot.on.chat_invite()
async def wrapper(ans: Message):
    # Raising when bot is invited to chat
    await ans('Hooray! Hi, friends!')


@bot.on.chat_mention()
async def wrapper(ans: Message):
    # Raising when bot is just mentioned, in one word
    await ans('I have been mentioned')


if __name__ == '__main__':
    bot.run()
