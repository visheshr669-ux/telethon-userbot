import os
import time
import asyncio
import urllib.request
from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

AUTO_REPLY_TEXT = """𝙑𝙞𝙨𝙝𝙪 𝙞𝙨 𝙘𝙪𝙧𝙧𝙚𝙣𝙩𝙡𝙮 𝙤𝙛𝙛𝙡𝙞𝙣𝙚.🚫
𝙎𝙞𝙡𝙚𝙣𝙘𝙚 𝙞𝙨𝙣'𝙩 𝙖𝙗𝙨𝙚𝙣𝙘𝙚—𝙞𝙩'𝙨 𝙛𝙤𝙘𝙪𝙨. 𝙇𝙚𝙖𝙫𝙚 𝙮𝙤𝙪𝙧 𝙢𝙚𝙨𝙨𝙖𝙜𝙚. 𝙄'𝙡𝙡 𝙧𝙚𝙥𝙡𝙮 𝙉𝙤𝙩 𝙚𝙫𝙚𝙧𝙮 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙙𝙚𝙨𝙚𝙧𝙫𝙚𝙨 𝙖𝙣 𝙞𝙣𝙨𝙩𝙖𝙣𝙩 𝙧𝙚𝙥𝙡𝙮. 𝙔𝙤𝙪𝙧𝙨 𝙝𝙖𝙨 𝙗𝙚𝙚𝙣 𝙧𝙚𝙘𝙚𝙞𝙫𝙚𝙙. 𝙬𝙝𝙚𝙣 𝙩𝙝𝙚 𝙩𝙞𝙢𝙚 𝙞𝙨 𝙧𝙞𝙜𝙝𝙩.𝙞𝙩 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙨𝙚𝙚𝙣💭"""

# Auto Inactivity Tracker for DM (10 Mins)
LAST_OUTGOING_TIME = time.time()
INACTIVITY_THRESHOLD = 600  # 10 Minutes

# Dictionary to track pending DM auto-replies
PENDING_DM_TASKS = {}

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string_session = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Supercell Magic Style Text Converter
def to_supercell(text):
    mapping = {
        'a': '𝗔', 'b': '𝗕', 'c': '𝗖', 'd': '𝗗', 'e': '𝗘', 'f': '𝗙', 'g': '𝗚', 'h': '𝗛',
        'i': '𝗜', 'j': '𝗝', 'k': '𝗞', 'l': '𝗟', 'm': '𝗠', 'n': '𝗡', 'o': '𝗢', 'p': '𝗣',
        'q': '𝗤', 'r': '𝗥', 's': '𝗦', 't': '𝗧', 'u': '𝗨', 'v': '𝗩', 'w': '𝗪', 'x': '𝗫',
        'y': '𝗬', 'z': '𝗭',
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛',
        'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '🇱', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣',
        'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫',
        'Y': '𝗬', 'Z': '𝗭',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
    }
    return "".join(mapping.get(c, c) for c in text)

def is_user_inactive():
    return (time.time() - LAST_OUTGOING_TIME) > INACTIVITY_THRESHOLD

# Track outgoing messages
@client.on(events.NewMessage(outgoing=True))
async def activity_tracker(event):
    global LAST_OUTGOING_TIME
    LAST_OUTGOING_TIME = time.time()
    chat_id = event.chat_id
    
    # Cancel DM pending task if user replied
    if event.is_private and chat_id in PENDING_DM_TASKS:
        PENDING_DM_TASKS[chat_id].cancel()
        del PENDING_DM_TASKS[chat_id]

# Private Chat Auto-Reply (10s timer + Smart Cancel)
@client.on(events.NewMessage(incoming=True))
async def pm_handler(event):
    if is_user_inactive() and event.is_private:
        sender = await event.get_sender()
        if sender and not sender.bot and not sender.is_self:
            chat_id = event.chat_id
            
            if chat_id in PENDING_DM_TASKS:
                PENDING_DM_TASKS[chat_id].cancel()

            async def delayed_pm_reply():
                try:
                    await asyncio.sleep(10) # 10 seconds timer
                    if is_user_inactive():
                        msg = await client.get_messages(chat_id, ids=event.id)
                        if msg and not msg.out:
                            await event.reply(AUTO_REPLY_TEXT)
                except asyncio.CancelledError:
                    pass
                finally:
                    if chat_id in PENDING_DM_TASKS:
                        del PENDING_DM_TASKS[chat_id]

            PENDING_DM_TASKS[chat_id] = asyncio.create_task(delayed_pm_reply())

# Supercell Font Command: .font <text>
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.font(?:\s+(.*))?'))
async def font_handler(event):
    input_text = event.pattern_match.group(1)
    
    if not input_text and event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg and reply_msg.text:
            input_text = reply_msg.text

    if not input_text:
        await event.edit("⚠️ **Usage:** `.font <text>` ya message reply karke `.font` likho.")
        return

    converted_text = f"⚔️ **{to_supercell(input_text)}** ⚡"
    await event.edit(converted_text)

# Self Command: .ping
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.ping$'))
async def ping_handler(event):
    start = time.time()
    msg = await event.edit("⚡ `Pinging...`")
    end = time.time()
    ms = round((end - start) * 1000)
    await msg.edit(f"🚀 **Pong!**\n⏱️ `Latency:` **{ms}ms**")

# Self Command: .alive
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.alive$'))
async def alive_handler(event):
    status_text = "💤 Inactive (Auto-AFK Active)" if is_user_inactive() else "🟢 Active & Online"
    alive_msg = (
        "⚙️ **𝙑𝙞𝙨𝙝𝙪 𝙐𝙨𝙚𝙧𝙗𝙤𝙩 𝙞𝙨 𝘼𝙡𝙞𝙫𝙚 & 𝙍𝙪𝙣𝙣𝙞𝙣𝙜!**\n\n"
        "👤 **Owner:** Vishesh\n"
        f"⚡ **Status:** {status_text}\n"
        "☁️ **Host:** Render Server\n"
        "⏱️ **Timer:** 10s (DM Smart Cancel Enabled)\n\n"
        "💭 *\"Silence isn't absence—it's focus.\"*"
    )
    await event.edit(alive_msg)

async def update_bio():
    ist = timezone(timedelta(hours=5, minutes=30))
    while True:
        try:
            now = datetime.now(ist)
            current_time = now.strftime("%I:%M %p")
            new_bio = f"⌚ {current_time} | 𝙎𝙞𝙡𝙚𝙣𝙘𝙚 𝙞𝙨𝙣'𝙩 𝙖𝙗𝙨𝙚𝙣𝙘𝙚—𝙞𝙩'𝙨 𝙛𝙤𝙘𝙪𝙨.⚡"
            await client(UpdateProfileRequest(about=new_bio))
        except Exception as e:
            print(f"Bio update error: {e}")
        await asyncio.sleep(60)

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
    asyncio.create_task(update_bio())
    yield
    await client.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "UserBot is live!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
