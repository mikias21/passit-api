import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('.env')

DB_HOST = os.getenv('DB_HOST')
client = MongoClient(DB_HOST)
users_collection = client.passit_main_db.users
users_signin_collection = client.passit_main_db.users_signin
users_verify_account_record = client.passit_main_db.users_verify_account_record
users_password_collection = client.passit_main_db.users_password
users_login_token_collection = client.passit_main_db.users_login_token_collection
users_deleted_passwords = client.passit_main_db.deleted_passwords
users_passwords_categories = client.passit_main_db.users_passwords_categories