import pytest

from vkbottle import CodeException, ErrorHandler, swear


def test_code_error():
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


@pytest.mark.asyncio
async def test_error_handler():
    class Base(Exception):
        pass

    class Derived(Base):
        pass

    error_handler = ErrorHandler()

    @error_handler.register_error_handler(Base)
    async def handler(error: Exception) -> int:
        assert isinstance(error, Derived)
        return 42

    assert await error_handler.handle(Derived()) == 42

    @error_handler.catch
    async def func() -> None:
        raise Derived()

    assert await func() == 42


@pytest.mark.asyncio
async def test_error_handler_with_code_exception():
    class CodeError(CodeException):
        pass

    error_handler = ErrorHandler()

    @error_handler.register_error_handler(*CodeError[1, 2])  # type: ignore
    async def handler(error: CodeError) -> None:
        assert isinstance(error, CodeError[1])

    await error_handler.handle(CodeError[1]())
