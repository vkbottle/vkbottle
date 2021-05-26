import asyncio

from vkbottle.http import AiohttpClient


async def main():
    http = AiohttpClient()
    print(await http.request_text("get", "https://google.com"))
    await http.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
