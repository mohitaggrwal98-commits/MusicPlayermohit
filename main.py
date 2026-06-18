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

# 2. Exact Original Bot Startup Logic
async def init():
    # Import inside function to allow Flask to start first without blocks
    from core.bot import AnniBot
    from core.userbot import assistants
    
    print("Starting AnniBot and Voice Stream...")
    await AnniBot.start()
    
    try:
        await AnniBot.stream_call.start()
    except Exception as e:
        print(f"Stream call status/error: {e}")
        
    for num in assistants:
        try:
            from core.userbot import assistants
            await assistants[num].start()
        except Exception as e:
            print(f"Assistant {num} error: {e}")
            
    print("Anni Music Player Bot Started and Plugins Loaded Successfully!")
    await idle()
    await AnniBot.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
    
