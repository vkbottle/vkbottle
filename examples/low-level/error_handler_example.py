from vkbottle import ErrorHandler
import asyncio

error_handler = ErrorHandler()


async def exc_handler(exc: RuntimeError):
    print("Oops error:", exc)


@error_handler.wraps_error_handler()
async def main():
    raise RuntimeError("Oh my god i am an exception")


error_handler.register_error_handler(RuntimeError, exception_handler=exc_handler)
asyncio.run(main())
