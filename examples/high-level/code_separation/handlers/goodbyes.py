from vkbottle.bot import BotLabeler, Message

labeler = BotLabeler()

# You can add auto_rules to labeler:
# labeler.auto_rules.append(SomeRule())
# You can change config for labeler locally:
# labeler.vbml_ignore_case = True


@labeler.message(text="пока")
async def bye_handler(message: Message):
    await message.answer("Пока...")


@labeler.message(text="до<!>свидания<!>")
async def goodbye_handler(message: Message):
    await message.answer("Надеюсь, скоро увидимся!")
