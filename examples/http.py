from vkbottle.http.client.aiohttp_client import AiohttpClient
import asyncio

http = AiohttpClient()

async def main():
    await http.request_text("get", "https://google.com")

asyncio.run(main())
