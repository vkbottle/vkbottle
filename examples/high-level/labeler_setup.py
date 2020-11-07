from vkbottle.bot import Bot, Message, BotLabeler
from vkbottle import ABCRule, BaseStateGroup, VKAPIError
from typing import List
import os


# A simple rule to demonstrate labeler
# setup for custom rules later
class SpamRule(ABCRule):
    def __init__(self, chars: List[str]):
        self.chars = "".join(chars)

    async def check(self, message: Message):
        return len(message.text) and message.text.strip(self.chars) == ""


# Create a bot, or a single labeler:
# from vkbottle.bot import BotLabeler
# labeler = BotLabeler()
bot = Bot(os.environ["token"])

# Labeler can be accessed with bot.labeler
# or with bot.on (.on is property which returns
# .labeler, this shortcut is cute legacy from
# vkbottle 2.x

# This is first shortcut for VBMLRule from custom_rules
# <vbml_ignore_case = True> makes get_vbml_rule to add
# re.IGNORECASE to flags
bot.labeler.vbml_ignore_case = True
# You can add default flags if ignore case is False
# <bot.labeler.default_flags = ...>

# We can add rule to custom_rules and it will be accessible
# in handlers in any place but is it of importance that
# labeler is always local (shortcuts work only for a local
# instance, for eg Bot, Blueprint, or pure Labeler)
bot.labeler.custom_rules["spam"] = SpamRule

# BotLabeler has fixed views. If you want to add yours you need
# to implement custom labeler, take it in account that labeler
# views are GLOBAL(!)
bot.labeler.views()  # {"message": MessageView, "raw": RawEventView}

bot.labeler.load(BotLabeler())  # Labeler can be loaded in another labeler

# Patcher for vbml rule shortcut can be set:
# <bot.labeler.patcher = ...>

# We will add some states
# The comments for states are skipped because
# we have another topic of the example
class SpamState(BaseStateGroup):
    GOOD = 1
    BAD = 2


# Lets add some handlers
@bot.on.chat_message(spam=["!", ".", "?", "$", "#", "@", "%"])
async def spam_handler(message: Message):
    state_peer = await bot.state_dispenser.get(message.from_id)

    if state_peer and state_peer.state == SpamState.BAD:
        try:
            await bot.api.messages.remove_chat_user(message.peer_id - 2e9, message.from_id)
            return "He dares to ignore me!"
        except VKAPIError(15):
            return "I hate myself"

    await message.answer("Pleease stop spamming..((")
    await bot.state_dispenser.set(message.from_id, SpamState.BAD)


@bot.on.message(text="forgive me")
async def forgive_handler(message: Message):
    await bot.state_dispenser.set(message.from_id, SpamState.GOOD)
    return "You are forgiven, my dear!"


bot.run_forever()
