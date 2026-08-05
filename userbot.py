import os
import http.server
import socketserver
import threading
from telethon import TelegramClient
from telethon.sessions import StringSession

# Render ke port scan error ko fix karne ke liye dummy server
def run_dummy_server():
    PORT = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Main Telethon UserBot Code
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

print("UserBot is starting...")
client.start()
print("UserBot is running successfully!")

client.run_until_disconnected()
