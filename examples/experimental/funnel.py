import dataclasses

from vkbottle.bot import Bot, Message

bot = Bot("")
bot.labeler.vbml_ignore_case = True

# imagine some database
records = {}


@dataclasses.dataclass
class Record:
    age: int
    t_shirt: str
    skills: str


@bot.on.message(text="хакатон")
async def funnel(m: Message):
    await m.answer("привет, сколько тебе лет?")

    async with bot.awaited_message(
        m, func=lambda msg: msg.text.isdigit(), default="надо ввести цифру"
    ) as m:
        age = int(m.text)

        if not 28 >= age >= 18:
            return "к сожалению, в хакатоне могут участвовать люди от 18 до 28"

    await m.answer("а какой у тебя размер футболки?")

    async with bot.awaited_message(
        m, text=["xs", "s", "m", "l", "xl"], default="надо ввести размер футболки, например: m"
    ) as m:
        t_shirt = m.text.lower()

    await m.answer("расскажи про свои умения, мы постараемся подобрать для тебя команду")

    async with bot.awaited_message(m, default="в текстовой форме расскажи о своих умениях") as m:
        skills = m.text

    await m.answer(f"тебе {age}, размер футболки {t_shirt}, умения: {skills}, все верно?")

    async with bot.awaited_message(m, text=["да", "нет"], default="да/нет") as m:
        if m.text.lower() == "нет":
            return "запись отменена"

    record = Record(age, t_shirt, skills)
    records[m.peer_id] = record
    return "записал"


bot.run_forever()
