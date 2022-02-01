from fastapi import BackgroundTasks, FastAPI, Request, Response
from handlers import bot, secret_key
from loguru import logger

app = FastAPI()

# token from vk for init callback server
confirmation_token: str


@app.on_event("startup")
async def startup_event():
    logger.info("Setup webhook")
    global confirmation_token
    confirmation_token = await bot.setup_webhook()


@app.post("/whateveryouwant")
async def vk_handler(req: Request, background_task: BackgroundTasks):
    try:
        data = await req.json()
    except:
        logger.warning("Empty request")
        return Response("not today", status_code=403)

    if data.get("type") == "confirmation":
        global confirmation_token
        logger.info(f"Send confirmation token: {confirmation_token}")
        return Response(confirmation_token)

    # If the secrets match, then the message definitely came from our bot
    if data.get("secret") == secret_key:
        # Running the process in the background, because the logic can be complicated
        background_task.add_task(bot.process_event, data)
    return Response("ok")
