from vkbottle.user import User
from vkbottle import TaskManager, VKError
import os, random, asyncio

user = User(os.environ["TOKEN"])


async def start_forwarding(peer_id: int, text: str):
    mid = await user.api.messages.send(peer_id=peer_id, message=text, random_id=random.randint(-2e9, 2e9))
    for i in range(200):
        try:
            await asyncio.sleep(1.8)
        except VKError:
            input("[Press after you input captcha] >> ")

tm = TaskManager(user.loop)
tm.add_task(start_forwarding(os.environ["PEER_ID"], os.environ["TEXT"]))
tm.run()
