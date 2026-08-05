import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.ping$'))
async def handler(event):
    await event.edit('**Pong! UserBot Active Hai! 🔥**')

print("Starting Telethon UserBot...")
client.start()
print("UserBot is online!")
client.run_until_disconnected()
