from flask import Flask
import threading
import os
import asyncio
import sys
from importlib import import_module
from pyrogram import idle
from pyrogram.types import BotCommand
from config import BANNED_USERS
from core.call import Anni
from core.mongo import db
from utils.inline import help_pannel

# 1. Flask Server for Render Port Binding
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Start Flask immediately in the background
threading.Thread(target=run_flask, daemon=True).start()

# 2. Asli Bot Logic
async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        sys.exit()
    await sys_db()
    for name in ALL_MODULES:
        import_module("plugins." + name)
    
    # Importing dynamically to avoid early init issues
    from plugins import ALL_MODULES
    from core.userbot import assistants
    import config
    from core.bot import AnniBot
    from utils.database import get_banned_users, get_gbanned

    await AnniBot.start()
    try:
        await AnniBot.stream_call.start()
    except Exception as e:
        LOGGER(__name__).error(f"Stream call error: {e}")
        
    for num in assistants:
        client = import_module(f"core.userbot").assistants[num]
        try:
            await client.start()
        except Exception as e:
            LOGGER(__name__).error(f"Assistant {num} failed to start: {e}")
            
    try:
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).error(f"Error loading banned users: {e}")
        
    LOGGER("AnniMusic").info(
        "Anni Music Player Bot Started Successfully."
    )
    await idle()
    await AnniBot.stop()
    for num in assistants:
        client = import_module(f"core.userbot").assistants[num]
        try:
            await client.stop()
        except:
            pass
    LOGGER("AnniMusic").info("Stopping Anni Music Player Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
    
