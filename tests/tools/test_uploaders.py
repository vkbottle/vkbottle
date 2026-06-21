import warnings
from io import BytesIO
from typing import Any

import pytest

from vkbottle.tools.uploader import (
    AudioUploader,
    DocMessagesUploader,
    DocUploader,
    VideoUploader,
)


class _FakeHTTP:
    async def request_text(self, url: str, method: str = "GET", data: Any = None, **kwargs: Any):
        return '{"upload_url": "http://upload", "file": "f"}'


class _FakeAPI:
    def __init__(self, responses: dict[str, Any] | None = None) -> None:
        self.http_client = _FakeHTTP()
        self.responses = responses or {}
        self.calls: list[tuple[str, dict]] = []

    async def request(self, method: str, data: Any = None):
        self.calls.append((method, dict(data) if data else {}))
        return self.responses.get(method, {"response": {}})


def test_uploader_deprecation_warning_points_to_caller():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        DocUploader(_FakeAPI(), generate_attachment_strings=True)

    assert len(caught) == 1
    # stacklevel=0 is invalid and makes the warning point at the warn() call inside the
    # library; a valid stacklevel points it at the caller instead.
    assert not caught[0].filename.endswith("uploader/base.py")


def test_get_bytes_io_explicit_name_wins():
    uploader = DocUploader(_FakeAPI())
    data = BytesIO(b"x")
    data.name = "original.bin"  # already carries a name

    result = uploader.get_bytes_io(data, name="wanted.jpg")

    # An explicitly requested name must override an existing BytesIO.name.
    assert result.name == "wanted.jpg"


@pytest.mark.asyncio
async def test_get_owner_id_falls_back_to_users_on_empty_groups():
    api = _FakeAPI(
        {
            "groups.getById": {"response": {"groups": []}},  # empty -> would IndexError
            "users.get": {"response": [{"id": 777}]},
        }
    )
    uploader = DocUploader(api)

    assert await uploader.get_owner_id() == 777


@pytest.mark.asyncio
async def test_get_owner_id_raises_clearly_when_unresolvable():
    api = _FakeAPI(
        {
            "groups.getById": {"response": {"groups": []}},
            "users.get": {"response": []},  # empty -> IndexError previously
        }
    )
    uploader = DocUploader(api)

    with pytest.raises(RuntimeError):
        await uploader.get_owner_id()


@pytest.mark.asyncio
async def test_doc_messages_upload_does_not_send_peer_id_to_save():
    api = _FakeAPI(
        {
            "docs.getMessagesUploadServer": {"response": {"upload_url": "http://u"}},
            "docs.save": {"response": {"type": "doc", "doc": {"owner_id": 1, "id": 2}}},
        }
    )
    uploader = DocMessagesUploader(api)

    await uploader.raw_upload(b"filedata", peer_id=123)

    save_call = next(d for m, d in api.calls if m == "docs.save")
    server_call = next(d for m, d in api.calls if m == "docs.getMessagesUploadServer")
    # peer_id is needed to get the messages upload server but is rejected by docs.save.
    assert "peer_id" not in save_call
    assert server_call.get("peer_id") == 123


@pytest.mark.asyncio
async def test_video_raw_upload_ignores_extra_params():
    api = _FakeAPI(
        {"video.save": {"response": {"owner_id": 1, "video_id": 2, "upload_url": "http://u"}}}
    )
    uploader = VideoUploader(api)

    # Extra params must not be forwarded to upload_files, which takes no **kwargs.
    result = await uploader.raw_upload(file_source=b"data", some_extra=1)

    assert result["video_id"] == 2


@pytest.mark.asyncio
async def test_audio_upload_handles_owner_id_in_save_response():
    api = _FakeAPI(
        {
            "audio.getUploadServer": {"response": {"upload_url": "http://u"}},
            "audio.save": {"response": {"id": 5, "owner_id": -10}},
        }
    )
    uploader = AudioUploader(api)

    # owner_id present in both the user params and the save response must not raise a
    # duplicate-keyword TypeError.
    result = await uploader.upload("artist", "title", b"data", owner_id=-10)

    assert result == "audio-10_5"
