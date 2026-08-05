import os
import asyncio
import urllib.request
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from telethon import TelegramClient, events
from telethon.sessions import StringSession

AUTO_REPLY_TEXT = """𝙑𝙞𝙨𝙝𝙪 𝙞𝙨 𝙘𝙪𝙧𝙧𝙚𝙣𝙩𝙡𝙮 𝙤𝙛𝙛𝙡𝙞𝙣𝙚.🚫
𝙎𝙞𝙡𝙚𝙣𝙘𝙚 𝙞𝙨𝙣'𝙩 𝙖𝙗𝙨𝙚𝙣𝙘𝙚—𝙞𝙩'𝙨 𝙛𝙤𝙘𝙪𝙨. 𝙇𝙚𝙖𝙫𝙚 𝙮𝙤𝙪𝙧 𝙢𝙚𝙨𝙨𝙖𝙜𝙚. 𝙄'𝙡𝙡 𝙧𝙚𝙥𝙡𝙮 𝙉𝙤𝙩 𝙚𝙫𝙚𝙧𝙮 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙙𝙚𝙨𝙚𝙧𝙫𝙚𝙨 𝙖𝙣 𝙞𝙣𝙨𝙩𝙖𝙣𝙩 𝙧𝙚𝙥𝙡𝙮. 𝙔𝙤𝙪𝙧𝙨 𝙝𝙖𝙨 𝙗𝙚𝙚𝙣 𝙧𝙚𝙘𝙚𝙞𝙫𝙚𝙙. 𝙬𝙝𝙚𝙣 𝙩𝙝𝙚 𝙩𝙞𝙢𝙚 𝙞𝙨 𝙧𝙞𝙜𝙝𝙩.𝙞𝙩 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙨𝙚𝙚𝙣💭"""

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def pm_handler(event):
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.bot and not sender.is_self:
            # 5 seconds delay before triggering auto-reply
            await asyncio.sleep(5)
            try:
                msg = await client.get_messages(event.chat_id, ids=event.id)
                if msg and not msg.out:
                    await event.reply(AUTO_REPLY_TEXT)
            except Exception:
                pass

async def keep_alive():
    url = os.environ.get("RENDER_EXTERNAL_URL")
    while True:
        await asyncio.sleep(240)
        if url:
            try:
                urllib.request.urlopen(url, timeout=10)
            except Exception:
                pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.start()
    asyncio.create_task(keep_alive())
    yield
    await client.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "UserBot is live!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
