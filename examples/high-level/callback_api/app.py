from fastapi import BackgroundTasks, FastAPI, Request, Response
from handlers import bot
from loguru import logger

app = FastAPI()

# token from vk for init callback server
confirmation_code: str
secret_key: str


@app.on_event("startup")
async def startup_event():
    logger.info("Setup webhook")
    global confirmation_code, secret_key
    confirmation_code, secret_key = await bot.setup_webhook()


@app.post("/whateveryouwant")
async def vk_handler(req: Request, background_task: BackgroundTasks):
    global confirmation_code, secret_key

    try:
        data = await req.json()
    except Exception:
        logger.warning("Empty request")
        return Response("not today", status_code=403)

    if data["type"] == "confirmation":
        logger.info("Send confirmation token: {}", confirmation_code)
        return Response(confirmation_code)

    # If the secrets match, then the message definitely came from our bot
    if data["secret"] == secret_key:
        # Running the process in the background, because the logic can be complicated
        background_task.add_task(bot.process_event, data)
    return Response("ok")
