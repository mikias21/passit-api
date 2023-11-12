import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('.env')

DB_HOST = os.getenv('DB_HOST')
client = MongoClient(DB_HOST)
users_collection = client.passit_main_db.users
