import pickle

from vkbottle import CaptchaError, ErrorHandler, VKAPIError


def test_vkapierror_pickle_roundtrip():
    err = VKAPIError[5](
        error_msg="boom",
        request_params=[{"key": "v", "value": "5.199"}, {"key": "method", "value": "x"}],
        extra="data",
    )
    restored = pickle.loads(pickle.dumps(err))

    assert isinstance(restored, VKAPIError)
    assert restored.code == 5
    assert restored.error_msg == "boom"
    # request_params survives as the already-normalized dict (no TypeError re-running __init__).
    assert restored.request_params == {"v": "5.199", "method": "x"}
    # Extra kwargs stay flat, not nested under a spurious "kwargs" key.
    assert restored.kwargs == {"extra": "data"}


def test_error_handler_prefers_most_specific_handler():
    handler = ErrorHandler()

    @handler.register_error_handler(VKAPIError)
    async def base_handler(error): ...

    @handler.register_error_handler(CaptchaError)
    async def captcha_handler(error): ...

    # CaptchaError is a VKAPIError, but its specific handler must win regardless of the
    # order handlers were registered in (dict insertion order must not shadow it).
    assert handler.lookup_handler(CaptchaError) is captcha_handler
    assert handler.lookup_handler(VKAPIError) is base_handler
