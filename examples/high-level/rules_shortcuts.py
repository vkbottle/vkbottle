# AndRule and OrRule can be replaced with simple
# tuple or set of rules. Tuple of rules is automatically
# converted to the OrRule and set is converted to
# the AndRule.

import os

from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import (
    AttachmentTypeRule,
    FromUserRule,
    MessageLengthRule,
    StickerRule,
)

bot = Bot(os.environ["token"])


# (1) StickerRule() handles all stickers.
# (2) MessageLengthRule handles all messages longer than or equal to 5 symbols.
# (3) FromUserRule handles messages sent from users.
# (4) AttachmentTypeRule will check if all attachments are of the same type
# If (1) or (2) is confirmed, (3) is confirmed and (4) not confirmed check is satisfied
@bot.on.message(
    StickerRule() | MessageLengthRule(5),
    FromUserRule(),
    ~AttachmentTypeRule("photo"),
)
async def greeting(message: Message):
    await message.answer("Привет!")


bot.run_forever()
