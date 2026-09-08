import asyncio
import traceback
import os, re, sys
from time import time
from io import StringIO
from MultiMedia import app
from pyrogram import filters
from config import OWNER_IDS
from inspect import getfullargspec
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# --------------------------------- utilites --------------------------------- #

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n")),
        globals(),
    )
    return await globals()["__aexec"](client, message)


async def edit_or_reply(msg, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


# --------------------------------- Eval/Dev --------------------------------- #

@app.on_edited_message(filters.command(["eval", "m"]) & filters.user(OWNER_IDS) & ~filters.forwarded & ~filters.via_bot)
@app.on_message(filters.command(["eval", "m"]) & filters.user(OWNER_IDS) & ~filters.forwarded & ~filters.via_bot)
async def executor(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>No command was given to execute!</b>")

    cmd = message.text.split(" ", maxsplit=1)[1]
    t1 = time()
    
    old_stderr, old_stdout = sys.stderr, sys.stdout
    sys.stdout, sys.stderr = StringIO(), StringIO()
    exc = None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout, stderr = sys.stdout.getvalue(), sys.stderr.getvalue()
    sys.stdout, sys.stderr = old_stdout, old_stderr

    evaluation = exc or stderr or stdout or "success"
    final_output = f"<b>📕 Result :</b>\n<pre language='python'>{evaluation}</pre>"
    t2 = time()

    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w", encoding="utf8") as out_file:
            out_file.write(str(evaluation))

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="⏳", callback_data=f"runtime {round(t2 - t1, 3)} Seconds")]]
        )
        await message.reply_document(
            document=filename,
            caption=f"<b>🔗 Eval :</b>\n<code>{cmd[:980]}</code>\n\n<b>📕 Result :</b>\nAttached document",
            quote=False,
            reply_markup=keyboard,
        )
        os.remove(filename)
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⏳", callback_data=f"runtime {round(t2 - t1, 3)} Seconds"),
                    InlineKeyboardButton(text="🗑", callback_data=f"forceclose abc|{message.from_user.id}"),
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


# --------------------------------- Regex Callback --------------------------------- #

@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)

@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, cq):
    callback_data = cq.data.strip().split(None, 1)[1]
    _, user_id = callback_data.split("|")
    
    if cq.from_user.id != int(user_id):
        return await cq.answer("You are not authorized to close this.", show_alert=True)
    await cq.message.delete()
    await cq.answer("Deleted!!", show_alert=True)


# --------------------------------- Shell --------------------------------- #

@app.on_message(filters.command("sh") & filters.user(OWNER_IDS) & ~filters.forwarded & ~filters.via_bot)
async def shellrunner(_, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>Example :</b>\n/sh git status")

    cmd_text = message.text.split(None, 1)[1]
    proc = await asyncio.create_subprocess_shell(
        cmd_text,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    output = (stdout + stderr).decode("utf-8", errors="replace").strip() or "No Output"

    if len(output) > 4096:
        filename = "output.txt"
        with open(filename, "w", encoding="utf8") as file:
            file.write(output)
        await message.reply_document(
            document=filename,
            caption="<code>Shell Output</code>"
        )
        os.remove(filename)
    else:
        await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>")

# --------------------------------- Update Bot --------------------------------- #

@app.on_message(filters.command("update") & filters.user(OWNER_IDS))
async def update(_, message):
    msg = await message.reply_text("Pulling changes from Git...", quote=True)
    
    proc = await asyncio.create_subprocess_shell(
        "git pull",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    
    if proc.returncode == 0:
        await msg.edit("Changes pulled successfully. Restarting bot...")
        os.execl(sys.executable, sys.executable, "-m", "MultiMedia")
    else:
        err = stderr.decode().strip()
        await msg.edit(f"<b>Git Pull Failed:</b>\n<pre>{err}</pre>")