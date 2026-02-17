from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv


load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")  
client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
fruits_collection = db.get_collection("fruits")
students_collection = db.get_collection("students")
user_collection = db.get_collection("users")
