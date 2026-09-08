import motor, sys, time
from MultiMedia import app, BOT_NAME
from config import OWNER_IDS
from pyrogram import filters
from MultiMedia.core.mongo import usersdb, premiumsdb


# --------------------------------------- Chat Watcher --------------------------------------- #

start_time = time.time()

@app.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        if message.from_user:
           if not await usersdb.is_user_exist(message.from_user.id):
             await usersdb.add_user(message.from_user.id)
    except:
        pass


# --------------------------------------- Bot Running Time --------------------------------------- #

def time_formatter():
    minutes, seconds = divmod(int(time.time() - start_time), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if tmp != "":
        if tmp.endswith(":"):
            return tmp[:-1]
        else:
            return tmp
    else:
        return "0 s"

# --------------------------------------- Stats Command --------------------------------------- #

@app.on_message(filters.command("stats") & filters.user(OWNER_IDS))
async def stats(client, message):
    start = time.time()
    users = len(await usersdb.get_all_users())
    ping = round((time.time() - start) * 1000)
    premiums = len(await premiumsdb.get_all_premiums())
    await message.reply_text(f"""
**Stats of** {BOT_NAME} :

🏓 **Ping Pong**: {ping}ms
📊 **Total Users** : `{users}`
🏵 **Premiums** : `{premiums}`
⚙️ **Bot Uptime** : `{time_formatter()}`
    
🎨 **Python Version**: `{sys.version.split()[0]}`
📑 **Mongo Version**: `{motor.version}`
""")
  
