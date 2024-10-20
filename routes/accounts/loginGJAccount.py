from . import accounts
from flask import request
from config import *
from database import *
from utils import *
from webhook import *

@accounts.route(f'{BASE_URL}/accounts/loginGJAccount.php', methods=['POST', 'GET'], strict_slashes=False)
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