from . import users
from config import BASE_URL
from utils import *
from flask import request
from database import *

@users.route(f'{BASE_URL}/getGJUserInfo20.php', methods=['POST', 'GET'], strict_slashes=False)  
def getGJUserInfo20():
    accountId = int(request.form.get('accountID')) if request.form.get('accountID') else None
    targetAccountId = int(request.form.get('targetAccountID'))
    print(targetAccountId)
    
    if accountId:
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
    return f"""1:{ao['username']}:2:{ao['id']}:3:{ao['stars']}:13:{ao['coins']}:17:{ao['user_coins']}:10:{ao['first_color']}:11:{ao['second_color']}:3:{ao['stars']}:52:{ao['moons']}:51:{ao['third_color']}:46:{ao['diamonds']}:4:{ao['demons']}:8:{ao['cp']}:18:{ao['mS']}:19:{ao['frS']}:50:{ao['cS']}:20:{ao['yt']}:21:{ao['icon_cube']}:22:{ao['icon_ship']}:23:{ao['icon_ball']}:24:{ao['icon_ufo']}:25:{ao['icon_wave']}:26:{ao['icon_robot']}:28:{ao['icon_glow']}:43:{ao['icon_spider']}:48:0:53:{ao['icon_copter']}:54:{ao['icon_jetpack']}:30:{ao['global_rank']}:16:{targetAccountId}:49:{ao['mod_badge']}:29:1""" # IM A FUCKING DUMBASS, EVERYTHING I HAD TO ADD IS 29:1 TO FIX THIS SHIT
