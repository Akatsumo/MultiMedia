import asyncio
import os, time, math, yt_dlp
from config import CHANNEL_IDS
from MultiMedia.core import script
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ------------------------------------------ Force-Subscribe ------------------------------------------ #

async def check_channel(app, channel, user_id):
    try:
        member = await app.get_chat_member(channel, user_id)
        if member.status in (ChatMemberStatus.BANNED, "kicked"):
            return "banned", None
        return "joined", None
    except UserNotParticipant:
        return "not_joined", await app.export_chat_invite_link(channel)
    except Exception:
        return "error", None

async def subscribe(app, message):
    if not message.from_user:
        return False

    results = await asyncio.gather(*(check_channel(app, ch, message.from_user.id) for ch in CHANNEL_IDS))
    buttons = []
    for status, link in results:
        if status == "banned":
            await message.reply_text("Sorry Sir, You are Banned. Contact My Support Group @DevsHubChat")
            return True
        if status == "error":
            await message.reply_text("Something Went Wrong. Contact My Support Group @DevsHubChat")
            return True
        if status == "not_joined":
            buttons.append([InlineKeyboardButton("📢 Join Channel", url=link)])

    if buttons:
        await message.reply_photo(
            photo="https://telegra.ph/file/b7a933f423c153f866699.jpg",
            caption=script.FORCE_MSG.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return True

    return False

        
# ------------------------------------------ Progress-Bar ------------------------------------------ #

PROGRESS_BAR = """\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗂️ : {1} | {2}
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣ """

# ------------------------------------------ Progress-Requirement ------------------------------------------ #

PROGRESS_CACHE = {}

def humanbytes(size):
    if not size: return "0 B"
    power, n, units = 1024, 0, [' ', 'Ki', 'Mi', 'Gi', 'Ti']
    while size >= power and n < 4: size /= power; n += 1
    return f"{size:.2f} {units[n]}B"

def time_formatter(seconds: int) -> str:
    if not seconds or seconds < 0: return "0s"
    m, s = divmod(int(seconds), 60); h, m = divmod(m, 60); d, h = divmod(h, 24)
    return " ".join(filter(None, [f"{d}d" if d else "", f"{h}h" if h else "", f"{m}m" if m else "", f"{s}s" if s or not (d or h or m) else ""]))

async def progress_bar(current, total, ud_type, message, start):
    now, diff = time.time(), time.time() - start
    if diff <= 0 or ((now - PROGRESS_CACHE.get(message.id, 0)) < 3.5 and current != total): return
    PROGRESS_CACHE[message.id], pct, speed = now, (current / total) * 100, current / diff
    eta = time_formatter(round((total - current) / speed) if speed > 0 else 0)
    bar = "█" * (filled := math.floor(pct / 10)) + "░" * (10 - filled)
    
    body = PROGRESS_BAR.format(
        f"{pct:.2f}",
        humanbytes(current),
        humanbytes(total),
        humanbytes(speed),
        eta if eta else "0s"
    )
    text = f"<b>{ud_type}</b>\n<code>[{bar}]</code>\n{body}"
    
    try: await message.edit_text(text=text)
    except FloodWait as e: PROGRESS_CACHE[message.id] = now + e.value
    except Exception: pass
    finally: (current == total) and PROGRESS_CACHE.pop(message.id, None)

# ------------------------------------------ Get-Video-Stream ------------------------------------------ #

async def get_download_media(link, file_name):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"downloads/{file_name}.%(ext)s",  
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }
    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, False)
    video = os.path.join("downloads", f"{file_name}.{info['ext']}" )
    if os.path.exists(video):
        return video
    x.download([link])
    return video
