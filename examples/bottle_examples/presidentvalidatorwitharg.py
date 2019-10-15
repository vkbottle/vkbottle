from vkbottler.vkbottle import Bot, Message, validators

bot = Bot('token', 1, debug=True, plugin_folder='examplebot')


class BottleValidators(validators.VBMLValidators):
    async def startswith(self, value: str, start: str):
        if value.startswith(start):
            return value


# Answer <Президент😎😎> to <!никнейм Ким-..>
@bot.on.message.lower('!президент <name:startswith[Ким]>')
async def wrapper(ans: Message, name):
    await ans(f'{name}😎😎')

bot.patcher(BottleValidators)
bot.run_polling()
