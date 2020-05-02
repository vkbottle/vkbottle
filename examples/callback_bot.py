from aiohttp.web import RouteTableDef, Application, Request, run_app

from vkbottle import Bot

app = Application()
routes = RouteTableDef()
bot = Bot("my-token")


@routes.get("/bot")
async def executor(request: Request):
    return await bot.emulate(
        event=dict(request.query), secret="my_secret", confirmation_token="my_confirmation"
    )


@bot.on.message(text="test", lower=True)
async def wrapper():
    return "test"


app.add_routes(routes)
run_app(app)
