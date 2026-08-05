import os
import http.server
import socketserver
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Render Port Fix
def run_dummy_server():
    PORT = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Self Test Command (.ping)
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.ping$'))
async def ping_handler(event):
    await event.edit('**Pong! UserBot Active Hai! 🔥**')

# Custom Auto Reply in DM
@client.on(events.NewMessage(incoming=True, private=True))
async def pm_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        sender = await event.get_sender()
        if sender and not sender.bot:
            await event.reply("Yooooo Vishu here!! wasupp !! See you within a minute!")

print("Starting Telethon UserBot...")
client.start()
print("UserBot is online!")
client.run_until_disconnected()
