from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_IDS = list(map(int, getenv("OWNER_IDS", "").split()))
MONGO_DB = getenv("MONGO_DB", "")
CHANNEL_IDS = list(map(int, getenv("CHANNEL_IDS", "").split()))

