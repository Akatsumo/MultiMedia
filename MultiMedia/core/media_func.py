import os, uuid, time, hashlib
import aiofiles, aiohttp, asyncio
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from MultiMedia import app
from MultiMedia.core import core_func


# ---------------------------------------- Make Requests ---------------------------------------- #

async def make_request(url: str, method: str = "GET", is_bytes: bool = False, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, **kwargs) as response:
            data = await response.read() if is_bytes else await response.json(content_type=None)        
            return response.status, data
                
# ---------------------------------------- Get Duration ---------------------------------------- #

def get_meta(path):
    try:
        p = createParser(path)
        m = extractMetadata(p) if p else None
        return (m.get("duration").seconds if m and m.has("duration") else 0,
                m.get("width") if m and m.has("width") else 1280,
                m.get("height") if m and m.has("height") else 720)
    except: return 0, 1280, 720
        
# ---------------------------------------- Download Thumbnail ---------------------------------------- #

async def get_thumb(url):
    status, data_bytes = await make_request(url, "GET", is_bytes=True)
    if status == 200:
        fn = f"{hashlib.md5(url.encode()).hexdigest()}.jpg"
        async with aiofiles.open(fn, 'wb') as f:
            await f.write(data_bytes)
        return fn
    return None

# ---------------------------------------- Media Uploader ---------------------------------------- #

async def media_uploader(message, download_url, title="", thumbnail=None):
    uid = f"{message.from_user.id}_{str(uuid.uuid4())[:8]}"
    msg = await message.reply_text("✨ Downloading...\n👀 Please wait a few seconds")
    video_path, thumb_path = None, None

    try:
        video_path = await core_func.get_download_media(download_url, f"{uid}_media_video")
        if not video_path or not os.path.exists(video_path):
            return await msg.edit_text("File Not Found !!\n\nNo Media was Downloaded.")

        duration, width, height = get_meta(video_path)
        if thumbnail:
            thumb_path = await get_thumb(thumbnail)
        else:
            thumb_path = f"{uid}_thumb.jpg"
            proc = await asyncio.create_subprocess_exec("ffmpeg", "-y", "-i", video_path, "-ss", "00:00:03", "-vframes", "1", thumb_path)
            await proc.wait()
            if not os.path.exists(thumb_path): thumb_path = None

        media = await app.send_video(
            chat_id=message.chat.id, video=video_path, caption=title or "",
            supports_streaming=True, height=height, width=width, duration=duration,
            thumb=thumb_path, progress=core_func.progress_bar, progress_args=('**UPLOADING:**\n', msg, time.time())
        )
        await msg.delete()
        return True

    except Exception as e:
        await msg.edit_text(f"**Error**: {e}")
        return False
    finally:
        for f in (video_path, thumb_path):
            if f and os.path.exists(f): os.remove(f)

# ---------------------------------------- Media API ---------------------------------------- #

async def media_indicator(message, url, media_type):
    api_url = "https://media-core-six.vercel.app/api/social-media" #don't change bro, its free
    status, data = await make_request(api_url, "POST", params={"url": url, "media_type": media_type}, timeout=15)
    
    if status == 200 and data and data.get("status") == 200 and data.get("download_url"):
        return await media_uploader(message, data["download_url"], data.get("title", ""), data.get("thumbnail", ""))
    
    return await message.reply_text("🛑 Something went wrong in API")









