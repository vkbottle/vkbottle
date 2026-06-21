import pytest

from vkbottle.http import AiohttpClient
from vkbottle.http import aiohttp as aiohttp_mod


class _FakeResp:
    status = 200


class _FakeReqCM:
    async def __aenter__(self):
        return _FakeResp()

    async def __aexit__(self, *exc):
        return False


def _patch_session(mocker):
    sessions = []

    class _FakeSession:
        def __init__(self, **kwargs):
            self.closed = False
            self.connector_owner = False
            sessions.append(self)

        def request(self, **kwargs):
            return _FakeReqCM()

        async def close(self):
            self.closed = True

    mocker.patch.object(aiohttp_mod, "ClientSession", _FakeSession)
    return sessions


@pytest.mark.asyncio
async def test_request_recreates_session_on_new_event_loop(mocker):
    sessions = _patch_session(mocker)
    client = AiohttpClient()

    async with client.request("http://x/") as response:
        assert response.status == 200
    first = client.session

    # Simulate the cached session being bound to a different (now-dead) loop, as
    # happens to the process-wide SingleAiohttpClient across asyncio.run() calls.
    client._session_loop = object()
    async with client.request("http://x/") as response:
        assert response.status == 200

    assert client.session is not first
    assert len(sessions) == 2


@pytest.mark.asyncio
async def test_request_recreates_closed_session(mocker):
    sessions = _patch_session(mocker)
    client = AiohttpClient()

    async with client.request("http://x/") as response:
        assert response.status == 200
    first = client.session

    await client.close()
    assert first.closed

    # A closed session must not be reused — a fresh one is created instead.
    async with client.request("http://x/") as response:
        assert response.status == 200

    assert client.session is not first
    assert len(sessions) == 2


def test_json_serialize_returns_str_under_orjson(mocker):
    client = AiohttpClient()
    # orjson.dumps returns bytes, but aiohttp's json_serialize must yield str.
    mocker.patch.object(client.json_processing_module, "dumps", return_value=b'{"a":1}')

    result = client._json_serialize({"a": 1})

    assert result == '{"a":1}'
    assert isinstance(result, str)
