from . import accounts
from flask import request
from config import *
from database import *
from utils import *
from webhook import *

@accounts.route(f'{BASE_URL}/accounts/registerGJAccount.php', methods=['POST', 'GET'], strict_slashes=False)
def registerGJAccount():
    username = request.form.get('userName')
    email = request.form.get('email')
    password = request.form.get('password')
    
    user_exists = user_name_exists(username)
    email_exists = user_email_exists(email)
    
    
    if not email.split('@')[1].lower() in WHITELIST_EMAILS:
        send_webhook('ОШИБКА РЕГИСТРАЦИИ: Неверный email')
        return "-6"
    
    if len(username) < 3 or len(username) > 15:
        send_webhook('ОШИБКА РЕГИСТРАЦИИ: Неверный логин')
        return "-4"

    if len(password) < 6 or len(password) > 20:
        send_webhook('ОШИБКА РЕГИСТРАЦИИ: Неверный пароль')
        return "-5"
    
    if user_exists:
        send_webhook('ОШИБКА РЕГИСТРАЦИИ: Пользователь с таким логином уже зарегистрирован')
        return "-2"
    
    if email_exists:
        send_webhook('ОШИБКА РЕГИСТРАЦИИ: Пользователь с таким email уже зарегистрирован')
        return "-3"
    
    print(f"""
Username: {username}
EMAIL: {email}
Password: {password}
          """)
    
    send_webhook(f"""УСПЕШНАЯ РЕГИСТРАЦИЯ
Username: {username}
EMAIL: {email}
Password: {password}""")
    
    add_user(username, password, email)
    
    return "1"