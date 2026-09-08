from pyrogram import filters
from MultiMedia import app
from config import OWNER_IDS
from datetime import datetime
from MultiMedia.core.mongo import premiumsdb
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Devs Laboratory {🇮🇳}", url="https://t.me/DevsLaboratory")]])

# ------------------------------------- Add Premium ------------------------------------- #

@app.on_message(filters.command("addpremium") & filters.user(OWNER_IDS))
async def add_premium(client, message):

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("Usage:\n/addpremium username duration\nExample: /addpremium @user 7days")

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            return await message.reply_text("Example (reply method):\n/addpremium 7days")
        duration = message.command[1]
    else:
        if len(message.command) < 3:
            return await message.reply_text("Usage:\n/addpremium username duration\nExample: /addpremium @user 7days")
        username = message.command[1]
        duration = message.command[2]
        user = await client.get_users(username)

    user_data = await premiumsdb.add_premium(user.id, duration)

    join = user_data["join_date"].strftime("%d %B %Y | %H:%M:%S")
    end = user_data["end_date"].strftime("%d %B %Y | %H:%M:%S")

    remaining = user_data["end_date"] - datetime.utcnow()
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    caption = f"""
🧩 **Premium Activated**

👤 Name: {user.mention}
🆔 User ID: `{user.id}`

📅 Joined On: {join}
⏳ Expires On: {end}
⌛ Remaining: {days}d {hours}h {minutes}m {seconds}s
"""

    photos = [p async for p in client.get_chat_photos(user.id, limit=1)]
    if photos:
        return await message.reply_photo(photos[0].file_id, caption=caption, reply_markup=buttons)
    else:
        return await message.reply_text(caption, reply_markup=buttons)


# ------------------------------------- check Premium ------------------------------------- #

@app.on_message(filters.command("check_premium") & filters.user(OWNER_IDS))
async def get_premium(client, message):

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("Usage:\n/check_premium username\nor reply to a user with /check_premium")
      
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    data = await premiumsdb.get_premium(user.id)

    if not data:
        return await message.reply_text(f"🛑 {user.mention} is not a premium user.")

    join = data["join_date"].strftime("%d %B %Y | %H:%M:%S")
    end = data["end_date"].strftime("%d %B %Y | %H:%M:%S")

    remaining = data["end_date"] - datetime.utcnow()
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    caption = f"""
🧩 **Premium Status**

👤 Name: {user.mention}
🆔 User ID: `{user.id}`

📅 Joined On: {join}
⏳ Expires On: {end}
⌛ Remaining: {days}d {hours}h {minutes}m {seconds}s
"""
    photos = [p async for p in client.get_chat_photos(user.id, limit=1)]
    if photos:
        return await message.reply_photo(photos[0].file_id, caption=caption, reply_markup=buttons)
    else:
        return await message.reply_text(caption, reply_markup=buttons)

# ------------------------------------- Remove Premium ------------------------------------- #

@app.on_message(filters.command("removepremium") & filters.user(OWNER_IDS))
async def remove_premium(client, message):

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("Usage:\n/removepremium username\nor reply to a user with /removepremium")

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    data = await premiumsdb.get_premium(user.id)
    if not data:
        return await message.reply_text(f"❌ {user.mention} is not a premium user.")
        
    await premiumsdb.remove_premium(user.id)

    caption = f"""
🧩 **Premium Removed**

👤 Name: {user.mention}
🆔 User ID: `{user.id}`

Status: Successfully downgraded to normal user.
"""
    photos = [p async for p in client.get_chat_photos(user.id, limit=1)]
    if photos:
        return await message.reply_photo(photos[0].file_id, caption=caption, reply_markup=buttons)
    else:
        return await message.reply_text(caption, reply_markup=buttons)
