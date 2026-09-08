from MultiMedia.core.mongo import database

# --------------------------- Users Collection --------------------------- #
usersdb = database.users_db

async def ensure_indexes():
    await usersdb.create_index("user", unique=True)


# --------------------------- Get All Users --------------------------- #
async def get_all_users():
    return [
        doc["user"]
        async for doc in usersdb.find(
            {"user": {"$gt": 0}},
            {"_id": 0, "user": 1}
        )
    ]


#  --------------------------- Check User Exists --------------------------- #
async def is_user_exist(user: int) -> bool:
    return bool(await usersdb.find_one({"user": user}))


# --------------------------- Add User --------------------------- #
async def add_user(user: int):
    await usersdb.update_one(
        {"user": user},
        {"$setOnInsert": {"user": user}},
        upsert=True
    )


# --------------------------- Delete User --------------------------- #
async def del_user(user: int):
    await usersdb.delete_one({"user": user})

    
