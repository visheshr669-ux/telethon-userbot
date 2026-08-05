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
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

threading.Thread(target=run_dummy_server, daemon=True).start()

# Telethon Config
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Simple Private DM Handler
@client.on(events.NewMessage(incoming=True))
async def pm_handler(event):
    if event.is_private:
        sender = await event.get_sender()
        # Ensure it's not a message sent by yourself and not from a bot
        if sender and not sender.bot and not sender.is_self:
            await event.reply("Yooooo Vishu here!! wasupp !! See you within a minute!")

print("Starting Telethon UserBot...")
client.start()
print("UserBot is active and listening to DMs!")
client.run_until_disconnected()
