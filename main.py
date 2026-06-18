from flask import Flask
import threading
import os
import asyncio
import sys

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

# 2. Your Actual Bot Imports & Logic
from pyrogram import Client
from pytgcalls import PyTgCalls
# Agar aapke project me baki files se imports hain toh unhe yahan likhein:
# from core.song import Song

async def main():
    print("Starting Bot...")
    # Apne bot ka main logic ya app.start() / idle() yahan likhein
    # Example:
    # app = Client("my_bot")
    # await app.start()
    # print("Bot Started Successfully!")
    
    # Keep the async loop running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
