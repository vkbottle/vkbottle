from vkbottle import Bot, Message

bot = Bot("token", 1, debug=True, plugin_folder="examplebot")

# Answer <Тебя зовут ИМЯ> to <!меня зовут ИМЯ>
@bot.on.message("!меня зовут <name>", lower=True)
async def wrapper(ans: Message, name):
    await ans(f"Тебя зовут {name}")


bot.run_polling()
