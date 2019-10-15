from vkbottler.vkbottle import Bot, Message

bot = Bot('token', 1, debug=True, plugin_folder='examplebot')

# Answer <Тебя зовут ИМЯ> to <!меня зовут ИМЯ>
@bot.on.message.lower('!меня зовут <name>')
async def wrapper(ans: Message, name):
    await ans(f'Тебя зовут {name}')

bot.run_polling()
