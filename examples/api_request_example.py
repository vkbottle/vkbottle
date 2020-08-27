from vkbottle.api import API
import asyncio
import os

api = API(os.environ["token"])


async def main():
    print(await api.request("users.get", {"user_ids": -1}))  # Single request

    # Multiple request for one session
    async for response in api.request_many(
        [api.APIRequest("users.get", {}), api.APIRequest("groups.get", {})]
    ):
        print(response)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
