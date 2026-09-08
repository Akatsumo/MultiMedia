import asyncio
from MultiMedia import app
from pyrogram import filters
from config import OWNER_IDS
from MultiMedia.core.mongo import premiumsdb
from MultiMedia.core import media_func, core_func

# --------------------------------- utilites --------------------------------- #

spam_db = set()
free_access = {}
FREE_LIMIT = 3

DOMAIN_MAP = {
    "instagram.com": "instagram",
    "pin.it": "pinterest",
    "pinterest": "pinterest",
    "reddit.com": "reddit",
    "snapchat.com": "snapchat",
    "facebook.com": "facebook",
    "threads.com": "threads",
    "x.com": "twitter",
    "twitter.com": "twitter",
    "tera": "terabox",
}

UNSUPPORTED_DOMAINS = ("zoom.us", "pornhub", "xnxx", "xhamster", "xvideos")

# --------------------------------- Func --------------------------------- #

async def process_link(message, url):
    user_id = message.from_user.id
    try:
        platform = next((plat for domain, plat in DOMAIN_MAP.items() if domain in url), None)
        
        if platform:
            await media_func.media_indicator(message, url, platform)
        elif any(x in url for x in UNSUPPORTED_DOMAINS):
            await media_func.media_uploader(message, url)
        else:
            await message.reply_text("🛑 Not Supported!")

    except Exception as e:
        print(f"Error: {e} - Link: {url}")
        await message.reply_text(f"🛑 Something went wrong.\n\nPlease report it @DevsHubChat\n\nError: {e}")
    finally:
        spam_db.discard(user_id)

# --------------------------------- Regex Link Finder --------------------------------- #

@app.on_message(filters.regex(r'https?://[^\s]+'))
async def multi_link(_, message):
    if not message.from_user:
        return
        
    user_id = message.from_user.id
    if user_id in spam_db:
        return await message.reply_text("⏳ Please wait, your previous request is processing...")

    if user_id not in OWNER_IDS:
        if free_access.get(user_id, 0) >= FREE_LIMIT:
            premium_user_ids = await premiumsdb.get_all_premiums()
            is_premium = any(p['user_id'] == user_id for p in premium_user_ids)
            
            if not is_premium:
                return await message.reply_text("🎷 Today's Free Trial Has Expired !!\n\nBuy Premium 🍃, Contact ~ @Akatsumo")

    if await core_func.subscribe(_, message) == 1:
        return

    spam_db.add(user_id)
    free_access[user_id] = free_access.get(user_id, 0) + 1
    asyncio.create_task(process_link(message, message.text))
