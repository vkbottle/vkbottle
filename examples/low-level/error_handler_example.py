from vkbottle import ErrorHandler
import asyncio

error_handler = ErrorHandler()

# You can set redirect_arguments to error_handler and they
# will be passed after exception to exception handler
# ---
# async def f(a, b): raise RuntimeError
# async def exc_h(exc: RuntimeError, a, b): ...


async def exc_handler(exc: RuntimeError):
    print("Oops error:", exc)


@error_handler.wraps_error_handler()
async def main():
    raise RuntimeError("Oh my god i am an exception")


error_handler.register_error_handler(RuntimeError, exception_handler=exc_handler)
asyncio.run(main())
