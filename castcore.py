import time, colorama
from flask import Flask, request
import hashlib
from database import *
from webhook import send_webhook
from utils import *

VERSION = '0.1'
u = "/gdps/datagds"

WHITELIST_EMAILS = ["gmail.com", "mail.ru", "inbox.ru", "yandex.ru", "yandex.by"]

colorama.init()
app = Flask(__name__)


@app.route('/')
def index():
    return 'what are you expecting here to be, huh?'



@app.route(f'{u}/accounts/registerGJAccount.php', methods=['POST', 'GET'], strict_slashes=False)
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


@app.route(f'{u}/accounts/loginGJAccount.php', methods=['POST', 'GET'], strict_slashes=False)
def loginGJAccount():
    username = request.form.get('userName')
    password = request.form.get('password')
    gjp = request.form.get('gjp2')
    
    print([s for s in request.form.items()])

    user_exists = user_name_exists(username)
    
    if 3 > len(username) > 15:
        return "-11"
    
    
    # PASSWORD CHECK
    if gjp not in [None, '']:
        if len(gjp) != 40:
            return "-1"
    else:
        if len(password) > 20:
            return "-11"
        
    if not user_exists:
        return "-11"
    
    user = get_account(username)
    print(user[3], user[2])
    if user[3] != gjp:
        return "-11"
    
    send_webhook(f"УСПЕШНЫЙ ВХОД: {username}")
    
    return f"{user[0]},{user[0]}"

        
@app.route(f'{u}/backupGJAccountNew.php', methods=['POST', 'GET'], strict_slashes=False)
def backupGJAccountNew():
    username = request.form.get('userName')
    password = request.form.get('password')
    accountId = int(request.form.get('accountID'))
    gjp = request.form.get('gjp2')
    
    is_gjp2 = False
    
    if gjp not in [None, '']:
        is_gjp2 = True
        password = gjp
        
    account = get_account(username)
        
    if accountId <= 0:
        if not user_name_exists(username):
            return "-1"
        else:
            accountId = account[0]
            
    if account[3] != gjp:
        return "-1"
    
    save_data = request.form.get('saveData')
    
    with open(f'./data/account/{accountId}.gdacc', 'w') as f:
        f.write(save_data)
        
    return "1"

print(f'CastCore - {VERSION} Running! [{time.strftime("%H:%M:%S")}]\n{colorama.Fore.GREEN}Made specifically for the FDPS project.{colorama.Fore.RESET}')