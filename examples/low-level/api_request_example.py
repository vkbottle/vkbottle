import asyncio
import os

from vkbottle.api import API

# Load token from system environment variable
# https://12factor.net/config
api = API(os.environ["TOKEN"])


async def main():
    print(await api.request("users.get", {}))  # Single request

    # Multiple request for one session
    async for response in api.request_many(
        (
            api.APIRequest("users.get", {}),
            api.APIRequest("groups.get", {}),
        )
    ):
        print(response)


asyncio.run(main())
