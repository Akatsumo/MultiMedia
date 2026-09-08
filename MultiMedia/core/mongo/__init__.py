from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB

# --------------------------- MongoDB Client --------------------------- #

mongo = AsyncIOMotorClient(MONGO_DB)
database = mongo.MultiMedia
