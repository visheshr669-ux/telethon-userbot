import os
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

print("UserBot is starting...")
client.start()
print("UserBot is running successfully!")

client.run_until_disconnected()
