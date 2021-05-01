import os
from typing import Any, List

from vkbottle_types.objects import UsersUserXtrCounters

from vkbottle import ABCHandler, ABCView, BaseMiddleware, CtxStorage
from vkbottle.bot import Bot, Message

bot = Bot(os.environ["token"])
dummy_db = CtxStorage()


class NoBotMiddleware(BaseMiddleware):
    async def pre(self, message: Message):
        return message.from_id > 0  # True / False


class RegistrationMiddleware(BaseMiddleware):
    async def pre(self, message: Message):
        user = dummy_db.get(message.from_id)
        if user is None:
            user = (await bot.api.users.get(message.from_id))[0]
            dummy_db.set(message.from_id, user)
        return {"info": user}


class InfoMiddleware(BaseMiddleware):
    async def post(
        self,
        message: Message,
        view: "ABCView",
        handle_responses: List[Any],
        handlers: List["ABCHandler"],
    ):
        if not handlers:
            return

        await message.answer(
            "Сообщение было обработано:\n\n" f"View - {view}\n\n" f"Handlers - {handlers}"
        )


@bot.on.message(lev="кто я")
async def who_i_am_handler(message: Message, info: UsersUserXtrCounters):
    await message.answer(f"Ты - {info.first_name}")


bot.labeler.message_view.register_middleware(NoBotMiddleware)
bot.labeler.message_view.register_middleware(RegistrationMiddleware)
bot.labeler.message_view.register_middleware(InfoMiddleware)
bot.run_forever()
