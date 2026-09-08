import re
from datetime import datetime, timedelta
from MultiMedia.core.mongo import database

# --------------------------- Premium Collection --------------------------- #
db = database.premium_db


# --------------------------- Duration Parser --------------------------- #
def parse_duration(duration: str):
    pattern = r"(\d+)(minutes?|hours?|days?|months?)"
    match = re.fullmatch(pattern, duration.lower())

    if not match:
        raise ValueError("Invalid duration format")

    value = int(match.group(1))
    unit = match.group(2)

    if "minute" in unit:
        return timedelta(minutes=value)

    elif "hour" in unit:
        return timedelta(hours=value)

    elif "day" in unit:
        return timedelta(days=value)

    elif "month" in unit:
        return timedelta(days=value * 30)


# --------------------------- ADD PREMIUM --------------------------- #
async def add_premium(user_id: int, duration: str):
    time_delta = parse_duration(duration)

    join_date = datetime.utcnow()
    end_date = join_date + time_delta

    data = {
        "user_id": user_id,
        "join_date": join_date,
        "end_date": end_date
    }

    await db.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True
    )

    return data


# --------------------------- GET PREMIUM (Auto Expire Check) --------------------------- #
async def get_premium(user_id: int):
    user = await db.find_one({"user_id": user_id})

    if not user:
        return None

    # Auto expire check
    if datetime.utcnow() >= user["end_date"]:
        await db.delete_one({"user_id": user_id})
        return None

    return user


# --------------------------- REMOVE PREMIUM --------------------------- #
async def remove_premium(user_id: int):
    await db.delete_one({"user_id": user_id})
    return True


# --------------------------- GET ALL PREMIUM USERS --------------------------- #
async def get_all_premiums():
    now = datetime.utcnow()

    # expired users clean (optional safety)
    await db.delete_many({"end_date": {"$lte": now}})

    users = []
    async for user in db.find():
        users.append(user)

    return users
