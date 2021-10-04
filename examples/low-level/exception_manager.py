import os
import asyncio

from vkbottle.exception_factory import VKAPIError
from vkbottle.api import API

api = API(os.environ["token"])


async def main():
    try:
        await api.users.get(user_ids=["123456789"])
    except VKAPIError[5]:
        print("Ой, неверный ключ доступа.")
    except VKAPIError[30]:
        print("Ой, у пользователя закрытый профиль.")
    except VKAPIError as e:
        print(f"Произошла ошибка {e.code}.")


asyncio.get_event_loop().run_until_complete(main())
