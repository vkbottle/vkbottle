import pickle

from vkbottle import VKAPIError


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
