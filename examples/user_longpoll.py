from vkbottle.user import User
from vkbottle.user.types import Message
from vkbottle.rule import VBMLUserRule

user = User("user-token", 123)
user.mode(8)


@user.on.message_new(VBMLUserRule("hi, <name>"))
async def wrapper(ans: Message, name):
    await ans(f"I'm not a {name}!")


@user.on.message_read_out()
async def call(event: dict):
    await user.api.request(
        "messages.send",
        {
            "message": "Ye! You finally read it!",
            "peer_id": event["peer_id"],
            "random_id": 0,
        },
    )


user.run_polling()
