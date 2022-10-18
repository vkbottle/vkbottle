from vkbottle import CodeException, swear


def test_code_exception():
    class CodeError(CodeException):
        pass

    try:
        raise CodeError[1]()
    except CodeError[2] as e:
        raise AssertionError() from e
    except CodeError[3, 4] as e:
        raise AssertionError() from e
    except CodeError[1, 2, 5] as e:
        assert e.code == 1


def test_swear_sync():
    def sync_exception_handler(e: Exception, a):
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
