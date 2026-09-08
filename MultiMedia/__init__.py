import config
from pyrogram import Client

# --------------------------------- Client --------------------------------- #

app = Client(
    ":MultiMedia:",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# --------------------------------- Global Variables --------------------------------- #

BOT_ID = None
BOT_NAME = None
BOT_USERNAME = None
