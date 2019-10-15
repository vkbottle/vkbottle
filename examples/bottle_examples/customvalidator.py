from vkbottler.vkbottle import Bot, Message, validators
import re

bot = Bot('token', 1, debug=True, plugin_folder='examplebot')


class BottleValidators(validators.VBMLValidators):
    async def nickname(self, value: str):
        if re.match(r'[a-z0-9_]{5,16}$', value):
            return value
        return False


# Answer <Никнейм NICKNAME прошел проверку||Никнейм не прошел проверку...> to <!никнейм НИКНЕЙМ>
@bot.on.message.lower('!никнейм <nickname:nickname>')
async def wrapper(ans: Message, nickname):
    if nickname:
        await ans(f'Никнейм <<{nickname}>> прошел проверку!')
    else:
        await ans('Никнейм не прошел проверку! '
                  'В нем должны быть только незаглавные символы латинского алфавита и цифры. '
                  'Длина ника - от 5 до 16 символов!')

bot.patcher(BottleValidators)
bot.run_polling()
