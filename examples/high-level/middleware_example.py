import os
from typing import Any, List

from vkbottle_types.objects import UsersUserXtrCounters

from vkbottle import ABCHandler, ABCView, BaseMiddleware, CtxStorage
from vkbottle.bot import Bot, Message

bot = Bot(os.environ["token"])
dummy_db = CtxStorage()


class NoBotMiddleware(BaseMiddleware):
    async def pre(self):
        if self.event.from_id < 0:
            self.stop("Groups are not allowed to use bot")


class RegistrationMiddleware(BaseMiddleware):
    async def pre(self):
        user = dummy_db.get(self.event.from_id)
        if user is None:
            user = (await bot.api.users.get(self.event.from_id))[0]
            dummy_db.set(self.event.from_id, user)
        self.send({"info": user})


class InfoMiddleware(BaseMiddleware):
    async def post(
        self,
        view: "ABCView",
        handle_responses: List[Any],
        handlers: List["ABCHandler"],
    ):
        if not handlers:
            return

        await self.event.answer(
            "Сообщение было обработано:\n\n" f"View - {view}\n\n" f"Handlers - {handlers}"
        )


@bot.on.message(lev="кто я")
async def who_i_am_handler(message: Message, info: UsersUserXtrCounters):
    await message.answer(f"Ты - {info.first_name}")


bot.labeler.message_view.register_middleware(NoBotMiddleware)
bot.labeler.message_view.register_middleware(RegistrationMiddleware)
bot.labeler.message_view.register_middleware(InfoMiddleware)
bot.run_forever()
