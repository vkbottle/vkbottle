from vkbottle.user import User, Message
from vkbottle import VKError
import os


# Add variable TOKEN to your env variables
user = User(os.environ["TOKEN"])


async def solve_captcha(e: VKError):
    # solving captcha
    method = e.method_requested
    method.kwargs = {"captcha_key": "key", "captcha_sid": e.raw_error["captcha_sid"]}
    await method(**e.params_requested)


@user.on.message_handler(commands=["spam", "спам"])
async def hi(ans: Message):
    for _ in range(10):
        await ans("spam")


user.error_handler.add_error_handler(14, solve_captcha)
user.run_polling()
