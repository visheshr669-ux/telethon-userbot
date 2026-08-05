import os
import asyncio
from fastapi import FastAPI
import uvicorn
from telethon import TelegramClient, events
from telethon.sessions import StringSession

app = FastAPI()

@app.get("/")
def home():
    return {"status": "UserBot is online and running!"}

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def pm_handler(event):
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.bot and not sender.is_self:
            await event.reply("Yooooo Vishu here!! wasupp !! See you within a minute!")

@app.on_event("startup")
async def startup_event():
    await client.start()
    print("Telethon Client Started Successfully!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
