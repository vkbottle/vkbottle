import asyncio

from vkbottle.http import AiohttpClient


async def main():
    http = AiohttpClient()
    print(await http.request_text("https://google.com"))
    await http.close()


asyncio.run(main())
