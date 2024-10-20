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

        
@app.route(f'{u}/database/accounts/backupGJAccountNew.php', methods=['POST', 'GET'], strict_slashes=False)
def backupGJAccountNew():
    accountId = int(request.form.get('accountID'))
    gjp = request.form.get('gjp2')
    
    send_webhook('БЭКАП АККАУНТА: ' + str(accountId))
    
    is_gjp2 = False
    
    if gjp not in [None, '']:
        is_gjp2 = True
        password = gjp
        
    account = get_account_by_id(accountId)
        
    if accountId <= 0:
        if not user_id_exists(accountId):
            return "-1"
        else:
            accountId = account[0]
            
    if account[3] != gjp:
        return "-1"
    
    save_data = request.form.get('saveData')
    
    with open(f'./data/account/{accountId}.gdacc', 'w') as f:
        f.write(save_data)
        
    return "1"


@app.route(f'{u}/database/accounts/syncGJAccountNew.php', methods=['POST', 'GET'], strict_slashes=False)
def syncGJAccountNew():
    accountId = int(request.form.get('accountID'))
    gjp = request.form.get('gjp2')
    
    send_webhook('СИНХРОНИЗАЦИЯ АККАУНТА: ' + str(accountId))
    
    is_gjp2 = False
    
    if gjp not in [None, '']:
        is_gjp2 = True
        password = gjp
        
    account = get_account_by_id(accountId)
        
    if accountId <= 0:
        if not user_id_exists(accountId):
            return "-1"
        else:
            accountId = account[0]
            
    if account[3] != gjp:
        return "-1"
    
    with open(f'./data/account/{accountId}.gdacc') as f:
        save_data = f.read()
        
    return save_data + ";21;30;a;a"


@app.route(f'{u}/updateGJUserScore22.php', methods=['POST', 'GET'], strict_slashes=False)
def updateGJUserScore22():
    accountId = int(request.form.get('accountID'))
    password = request.form.get('gjp')
    gjp = request.form.get('gjp2')
    
    is_gjp2 = False
    
    if gjp not in [None, '']:
        is_gjp2 = True
        password = gjp
        
    if not user_id_exists(accountId):
        return "-1"
    
    user = get_account_by_id(accountId)
    
    if user[3] != password:
        return "-1"
    
    data = {}
    
    for item in request.form.items():
        data[item[0]] = item[1]
        
    # ADD LIMIT CHECKING AHHH
    
    cursor.execute("SELECT 1 FROM accounts WHERE id = %s", (accountId,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute("""
            INSERT INTO accounts (
                id, username, moons, demons, diamonds, user_coins, coins, 
                icon_id, icon_type, icon_cube, icon_ship, icon_ball, icon_wave, 
                icon_robot, icon_copter, icon_jetpack, icon_glow, first_color, second_color
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s
            )
        """, (
            accountId, data['userName'], data['moons'], data['demons'], 
            data['diamonds'], data['userCoins'], data['coins'], 
            data['accIcon'], data['iconType'], data['accIcon'], 
            data['accShip'], data['accBall'], data['accDart'], 
            data['accRobot'], data['accSwing'], data['accJetpack'], 
            data['accGlow'], data['color1'], data['color2']
        ))
        
    else:
        cursor.execute("""
        UPDATE accounts SET 
            username = %s, moons = %s, demons = %s, diamonds = %s, 
            user_coins = %s, coins = %s, icon_id = %s, icon_type = %s, 
            icon_cube = %s, icon_ship = %s, icon_ball = %s, icon_wave = %s,
            icon_robot = %s, icon_copter = %s, icon_jetpack = %s, icon_glow = %s, first_color = %s, second_color = %s
        WHERE id = %s
        """, (
            data['userName'], data['moons'], data['demons'],
            data['diamonds'], data['userCoins'], data['coins'],
            data['accIcon'], data['iconType'], data['accIcon'],
            data['accShip'], data['accBall'], data['accDart'],
            data['accRobot'], data['accSwing'], data['accJetpack'],
            data['accGlow'], data['color1'], data['color2'], accountId
        ))


    
    return str(user[0])


@app.route(f'{u}/getGJUserInfo20.php', methods=['POST', 'GET'], strict_slashes=False)  
def getGJUserInfo20():
    accountId = int(request.form.get('accountID'))
    targetAccountId = int(request.form.get('targetAccountID'))
    password = request.form.get('gjp')
    gjp = request.form.get('gjp2')
    
    is_gjp2 = False
    
    if gjp not in [None, '']:
        is_gjp2 = True
        password = gjp
        
    if targetAccountId <= 0 or accountId <= 0:
        return "-1"
    
    user = get_account_by_id(accountId)
    
    if user[3] != password:
        return "-1"
    
    dict_cursor.execute("SELECT * FROM accounts WHERE id = %s", (targetAccountId,))
    ao = dict_cursor.fetchone()
    print(ao)
    return f"""1:{ao['username']}:2:{ao['id']}:3:{ao['stars']}:13:{ao['coins']}:17:{ao['user_coins']}:10:{ao['first_color']}:11:{ao['second_color']}:3:{ao['stars']}:52:{ao['moons']}:51:{ao['third_color']}:46:{ao['diamonds']}:4:{ao['demons']}:8:{ao['cp']}:18:{ao['mS']}:19:{ao['frS']}:50:{ao['cS']}:20:{ao['yt']}:21:{ao['icon_cube']}:22:{ao['icon_ship']}:23:{ao['icon_ball']}:24:{ao['icon_ufo']}:25:{ao['icon_wave']}:26:{ao['icon_robot']}:28:{ao['icon_glow']}:43:{ao['icon_spider']}:48:0:53:{ao['icon_copter']}:54:{ao['icon_jetpack']}:30:{ao['global_rank']}:16:{accountId}:49:{ao['mod_badge']}:29:1""" # IM A FUCKING DUMBASS, EVERYTHING I HAD TO ADD IS 29:1 TO FIX THIS SHIT


@app.route(f"{u}/getGJAccountComments20.php", methods=['POST', 'GET'], strict_slashes=False)
def getGJAccountComments20():
    return "2~Q2FzdENvcmUgdGVzdCEgVmVyIDAuMSBydW5uaW5n~4~11~9~3 months~6~18083050#0:0:0"


@app.route(f"{u}/getAccountURL.php", methods=['POST', 'GET'], strict_slashes=False)
def getAccountURL():
    return 'http://localhost:5000/gdps/datagds'


print(f'CastCore - {VERSION} Running! [{time.strftime("%H:%M:%S")}]\n{colorama.Fore.GREEN}Made specifically for the FDPS project.{colorama.Fore.RESET}')
