from vkbottle import SessionManager, AiohttpClient
import pytest

@pytest.mark.asyncio
async def test_client():
    client = AiohttpClient()
    text = await client.request_text("GET", "https://google.com")
    await client.close()
    assert text

@pytest.mark.asyncio
async def test_session_manager():
    session_manager = SessionManager()
    async with session_manager as session:
        text = await session.request_text("GET", "https://google.com")
    assert text
