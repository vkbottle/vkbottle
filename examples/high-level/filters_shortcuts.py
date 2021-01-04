# AndFilter and OrFilter can be replaced with simple
# tuple or set of rules. Tuple of rules is automatically
# converted to the OrFilter and set is converted to
# the AndFilter.

import os

from vkbottle.bot import Bot, Message, rules

bot = Bot(os.environ["token"])

# (1) StickerRule() handles all stickers. (2) MessageLengthRule
# handles all messages longer than or equal to 5 symbols. (3)
# FromUserRule handles messages sent from users.
# If (1) or (2) is confirmed and (3) is confirmed check is
# satisfied
@bot.on.message((rules.StickerRule(), rules.MessageLengthRule(5)), rules.FromUserRule())
async def greeting(message: Message):
    await message.answer("Привет!")


bot.run_forever()
