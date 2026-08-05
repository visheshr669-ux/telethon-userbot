import os
import http.server
import socketserver
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Render Port Scanning Handler
def run_dummy_server():
    PORT = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Port server error: {e}")

threading.Thread(target=run_dummy_server, daemon=True).start()

# Telethon Details
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Incoming DM Handler
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_handler(event):
    sender = await event.get_sender()
    me = await client.get_me()
    if sender and not sender.bot and sender.id != me.id:
        await event.reply("Yooooo Vishu here!! wasupp !! See you within a minute!")

print("Userbot is initiating connection...")
client.start()
print("Userbot is online and listening!")
client.run_until_disconnected()
