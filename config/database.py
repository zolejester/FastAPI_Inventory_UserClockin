# Configuring MongoDB as DB
from pymongo import MongoClient
import os

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# MongoDB
db = client.v1_database

# Collections for user clockin & items
items_collection = db["items_collection"]
user_clockin_collection = db["user_clockin_collection"]
