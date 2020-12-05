from vkbottle.bot import Blueprint, Message

bp = Blueprint()

# You can add auto_rules to blueprint labeler:
# bp.labeler.auto_rules.append(SomeRule())
# You can change config for blueprint labeler locally:
# bp.labeler.ignore_case = True


@bp.on.message(text="пока")
async def bye_handler(message: Message):
    await message.answer("Пока...")


@bp.on.message(text="до<!>свидания<!>")
async def goodbye_handler(message: Message):
    await message.answer("Надеюсь, скоро увидимся!")
