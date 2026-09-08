import asyncio
import importlib, MultiMedia
from pyrogram import idle 
from MultiMedia.modules import ALL_MODULES

loop = asyncio.get_event_loop()

async def init_bot():
    await MultiMedia.app.start()
    print("[√] Bot Started")
    
    getme = await MultiMedia.app.get_me()
    MultiMedia.BOT_ID = getme.id
    MultiMedia.BOT_USERNAME = getme.username
    MultiMedia.BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name
    print(f"»» Booted as {MultiMedia.BOT_NAME} (@{MultiMedia.BOT_USERNAME})")
  
# ------------------------------- LOAD MODULES ------------------------------- #
    for all_module in ALL_MODULES:
        importlib.import_module("MultiMedia.modules." + all_module)

    print("[√] Bot Deploy Successful ✨")
    await idle()
    await MultiMedia.app.stop()
    print("Bot Stopped!!")


if __name__ == "__main__":
    loop.run_until_complete(init_bot())
