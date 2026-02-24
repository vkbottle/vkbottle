import os

from vkbottle.bot import Bot, Message

bot = Bot(os.environ["TOKEN"])


async def process_foreign_messages(message: Message) -> str:
    """Recursively processes forwarded messages, loading full content for each."""
    lines = []

    async def walk(fwd_messages, depth=0):
        for fwd in fwd_messages:
            # Load full message data (attachments, full text, etc.)
            await fwd.get_full_message()

            prefix = "  " * depth
            attachments = fwd.get_attachment_strings() or []

            lines.append(
                f"{prefix}[{fwd.from_id}]: {fwd.text}"
                + (f" (attachments: {', '.join(attachments)})" if attachments else "")
            )

            if fwd.fwd_messages:
                await walk(fwd.fwd_messages, depth + 1)

    if message.reply_message:
        await message.reply_message.get_full_message()
        lines.append(f"Reply to [{message.reply_message.from_id}]: {message.reply_message.text}")

    if message.fwd_messages:
        await walk(message.fwd_messages)

    return "\n".join(lines)


@bot.on.message()
async def handler(message: Message):
    if not message.fwd_messages and not message.reply_message:
        return

    result = await process_foreign_messages(message)
    await message.answer(f"Forwarded messages:\n{result}")


bot.run_forever()
