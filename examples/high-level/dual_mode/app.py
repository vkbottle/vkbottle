import asyncio
from contextlib import suppress

from bot import bot
from fastapi import BackgroundTasks, FastAPI, Request, Response
from loguru import logger

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.info("Setting up Callback API and starting Long Poll")
    app.state.confirmation_code, app.state.secret_key = await bot.setup_webhook()
    app.state.polling_task = asyncio.create_task(bot.run_polling())


@app.on_event("shutdown")
async def shutdown_event():
    polling_task: asyncio.Task | None = getattr(app.state, "polling_task", None)
    if polling_task is None:
        return
    polling_task.cancel()
    with suppress(asyncio.CancelledError):
        await polling_task


@app.post("/whateveryouwant")
async def vk_handler(req: Request, background_task: BackgroundTasks):
    try:
        data = await req.json()
    except Exception:
        logger.warning("Empty request")
        return Response("not today", status_code=403)

    if data.get("secret") != app.state.secret_key:
        logger.warning("Callback request with an invalid secret")
        return Response("not today", status_code=403)

    if data.get("type") == "confirmation":
        logger.info("Sending Callback API confirmation code")
        return Response(app.state.confirmation_code)

    # ``dual_mode=True`` in bot.py atomically drops a duplicate received from Long Poll.
    background_task.add_task(bot.process_event, data)
    return Response("ok")
