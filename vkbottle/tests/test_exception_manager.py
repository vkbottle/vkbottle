from vkbottle import CodeErrorFactory, SingleError, swear


def test_exc_manager_code_error():
    exc_manager = CodeErrorFactory()

    try:
        raise exc_manager(7)
    except exc_manager(6):
        assert False
    except exc_manager(7):
        return
    except exc_manager():
        assert False


def test_exc_manager_single_error():
    class SomeError(SingleError):
        pass

    try:
        raise SomeError("Some error occurred")
    except SomeError:
        pass
    except BaseException:
        assert False


def test_swear_sync():
    def sync_exception_handler(e: BaseException, a):
        assert isinstance(e, RuntimeError)
        return a

    @swear(RuntimeError, just_return=True)
    def sync_just_return(a):
        raise RuntimeError(f"Error#{a}")

    @swear(RuntimeError, exception_handler=sync_exception_handler)
    def sync_with_exc_handler(a):
        raise RuntimeError(f"Error#{a}")

    assert sync_just_return(2)
    assert sync_with_exc_handler(3) == 3
