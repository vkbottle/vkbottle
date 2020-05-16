from vkbottle.user import User, Message
from vkbottle import VKError
from vkbottle.utils import logger
import aiohttp
import asyncio
import random
import os


# Add variable TOKEN to your env variables
user = User(os.environ["TOKEN"])


@user.error_handler.captcha_handler
async def solve_captcha(e: VKError):
    logger.error("Captcha. Solving...")
    async with aiohttp.ClientSession() as session:
        async with session.get(e.raw_error["captcha_img"]) as response_image:
            image = await response_image.content.read()
        async with session.post(
            "https://rucaptcha.com/in.php",
            data={"key": os.environ["RUCAPTCHA_TOKEN"], "file": image},
        ) as response_wait:
            result_id = (await response_wait.text()).split("|")[1]
        await asyncio.sleep(5)
        async with session.get(
            "https://rucaptcha.com/res.php",
            params={
                "key": os.environ["RUCAPTCHA_TOKEN"],
                "id": result_id,
                "action": "get",
            },
        ) as result:
            key = (await result.text()).split("|")[1]
    logger.success(f"Captcha was solved. Key: {key}")
    return key


async def rps_limit(e: VKError):
    await asyncio.sleep(1)
    return await e.method_requested(**e.params_requested)


@user.on.message_handler(text=["/t <text>"])
async def hi(ans: Message, text: str):
    message_id = await ans("|")
    new_text = ""
    for symbol in list(text):
        new_text += symbol
        await user.api.messages.edit(ans.peer_id, message_id, new_text + "|")
        await asyncio.sleep(1)
        if random.randint(0, 100) > 50:
            await user.api.messages.edit(ans.peer_id, message_id, new_text)
            await asyncio.sleep(1)


user.error_handler.add_error_handler(6, rps_limit)
user.run_polling()
