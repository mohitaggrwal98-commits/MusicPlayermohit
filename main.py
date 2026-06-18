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

# 2. Simplified Bot Logic to prevent crash
async def init():
    # Dynamic imports to prevent startup failures
    try:
        from core.bot import AnniBot
    except ImportError:
        print("Error: Could not import AnniBot from core.bot")
        sys.exit(1)
        
    try:
        from core.userbot import assistants
    except ImportError:
        assistants = {}

    print("Starting AnniBot...")
    await AnniBot.start()
    
    try:
        await AnniBot.stream_call.start()
    except Exception:
        pass
        
    for num in assistants:
        try:
            from core.userbot import assistants
            await assistants[num].start()
        except Exception:
            pass
            
    print("Anni Music Player Bot Started Successfully!")
    await idle()
    await AnniBot.stop()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(init())
    except KeyboardInterrupt:
        sys.exit(0)
        
