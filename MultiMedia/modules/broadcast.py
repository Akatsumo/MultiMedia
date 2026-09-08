import asyncio, traceback
from pyrogram import filters
from config import OWNER_IDS
from MultiMedia import app
from MultiMedia.core.mongo import usersdb
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

STOP_BROADCAST = False

# --------------------------------- utilites --------------------------------- #

async def send_msg(client, user_id, message, forward=False):
    try:
        if forward:
            await client.forward_messages(chat_id=user_id, from_chat_id=message.chat.id, message_ids=message.id)
        else:
            await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(client, user_id, message, forward)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : invalid\n"
    except Exception:
        return 500, traceback.format_exc()

# --------------------------------- Broadcast or Announce --------------------------------- #

@app.on_message(filters.command(["broadcast", "announce", "stop"]) & filters.user(OWNER_IDS))
async def broadcast_handler(client, message):
    global STOP_BROADCAST

    cmd = message.command[0]
    if cmd == "stop":
        STOP_BROADCAST = True
        return await message.reply_text("🛑 Broadcast stopped!")

    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to send.")

    STOP_BROADCAST = False
    forward = True if cmd == "announce" else False
    mode = "Forwarding" if forward else "Copying"
    exmsg = await message.reply_text(f"{mode} started...")
    users = await usersdb.get_all_users() or []
    done_users = 0
    failed_users = 0

    for user in users:
        if STOP_BROADCAST:
            break
        status, _ = await asyncio.create_task(send_msg(client, int(user), message.reply_to_message, forward))
        if status == 200:
            done_users += 1
        else:
            failed_users += 1
        await asyncio.sleep(0.1)

    await exmsg.edit_text(
        f"✅ Process Completed\n\n"
        f"📤 Mode: {'Forward' if forward else 'Copy'}\n"
        f"✔ Sent: `{done_users}` users\n"
        f"❌ Failed: `{failed_users}` users\n\n"
        f"{'🛑 Stopped manually' if STOP_BROADCAST else ''}"
    )
