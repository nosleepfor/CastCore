import mysql.connector
import time
from utils import *
import json
from dotenv import load_dotenv
import os

load_dotenv('.env')

config = json.load(open('config.json'))

db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME'),
    autocommit=True
)

cursor = db.cursor()
dict_cursor = db.cursor(dictionary=True)

def add_user(username, password, email):
    gjp = gen_gjp2(password, bcrypt=True)
    
    cursor.execute("INSERT INTO users (id, username, password, gjp2, email, date, is_banned, is_true) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (None, username, hash_passw(password), gjp, email, int(time.time()), 0, config['autoActivate']))
    
def user_email_exists(email):
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone() is not None

def user_name_exists(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone() is not None

def user_id_exists(id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    return cursor.fetchone() is not None

def get_account(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()

def get_account_by_id(id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    return cursor.fetchone()