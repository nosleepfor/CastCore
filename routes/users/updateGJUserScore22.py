from . import users
from config import BASE_URL
from utils import *
from flask import request
from database import *

@users.route(f'{BASE_URL}/updateGJUserScore22.php', methods=['POST', 'GET'], strict_slashes=False)
def updateGJUserScore22():
    accountId = int(request.form.get('accountID')) if request.form.get('accountID') else None
    if accountId:
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
    else:
        return '0'