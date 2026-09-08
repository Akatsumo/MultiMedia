from MultiMedia import app
from pyrogram import filters
from datetime import datetime
from MultiMedia.core import script, core_func
from MultiMedia.core.mongo import premiumsdb
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton




buttons = InlineKeyboardMarkup([
                [
                  InlineKeyboardButton("ᴀ ʙ ᴏ ᴜ ᴛ", callback_data="about_")
                ],[
                  InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/DevsHubChat"),
                  InlineKeyboardButton("🧩 ɪɴғᴏ", callback_data="info_")
                ]])



back_button  = [[
                    InlineKeyboardButton("ʙ ᴀ ᴄ ᴋ", callback_data="home_"),                    
                ]]


@app.on_message(filters.command("start"))
async def start(_,message):
  if await core_func.subscribe(_, message):
    return
  await message.reply_photo(photo="https://graph.org/file/3d2648d03644611ce8f54-52ace119f710560ebe.jpg", 
        caption=script.START_TXT.format(message.from_user.mention),
        reply_markup=buttons)



@app.on_callback_query()
async def handle_callback(_, query):
    user_id = query.from_user.id
    name = query.from_user.first_name
  
    if query.data == "home_":
        await query.message.edit_text(
            script.START_TXT.format(query.from_user.mention),
            reply_markup=buttons
        )

    elif query.data == "about_":
        reply_markup = InlineKeyboardMarkup(back_button)
        await query.message.edit_text(
            script.ABOUT_TXT,
            reply_markup=reply_markup
        )

    elif query.data == "info_":

        user_data = await premiumsdb.get_premium(user_id)

        if not user_data:
            return await query.answer("You are not premium user!!", show_alert=True)

        join = user_data["join_date"].strftime("%d %B %Y | %H:%M:%S")
        end = user_data["end_date"].strftime("%d %B %Y | %H:%M:%S")

        remaining = user_data["end_date"] - datetime.utcnow()

        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        Premium_text = f"""
🏵 Premium Details 🏵

🧩 Name: {name}
👤 User ID: {user_data['user_id']}

📅 Joined On: {join}
⏳ Expires On: {end}
⌛️ Time Remaining: {days}d {hours}h {minutes}m {seconds}s
"""

        await query.answer(Premium_text, show_alert=True)

    elif query.data == "maintainer_":
        await query.answer("Coming soon... Bot under maintenance", show_alert=True)







