# Configuring MongoDB as DB
from pymongo import MongoClient
import os

mongodb_user = os.getenv("MONGODB_USER")
mongodb_password = os.getenv("MONGODB_PASSWORD")

client = MongoClient("mongodb+srv://f{mongodb_user}:f{mongodb_password}@cluster0.ykzion4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# MongoDB
db = client.v1_database

# Collections for user clockin & items
items_collection = db["items_collection"]
user_clockin_collection = db["user_clockin_collection"]
