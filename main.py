from flask import Flask
import threading
import os
import asyncio
import sys
from importlib import import_module
from pyrogram import idle

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
    import config
    from plugins import ALL_MODULES
    from core.userbot import assistants
    from core.bot import AnniBot

    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        sys.exit()

    for name in ALL_MODULES:
        import_module("plugins." + name)
    
    await AnniBot.start()
    try:
        await AnniBot.stream_call.start()
    except Exception:
        pass
        
    for num in assistants:
        client = import_module(f"core.userbot").assistants[num]
        try:
            await client.start()
        except Exception:
            pass
            
    print("Anni Music Player Bot Started Successfully.")
    await idle()
    await AnniBot.stop()
    for num in assistants:
        client = import_module(f"core.userbot").assistants[num]
        try:
            await client.stop()
        except:
            pass

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
