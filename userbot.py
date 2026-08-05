from telethon import TelegramClient, events

api_id = 32073948
api_hash = "a1815a567509a71bb138592c03b9984f"

client = TelegramClient("userbot", api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private and not event.out:
        await event.reply("Hey! I'm offline right now. I'll reply soon.")

client.start()
print("UserBot is running...")
client.run_until_disconnected()

