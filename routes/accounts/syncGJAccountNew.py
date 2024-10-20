from . import accounts
from flask import request
from config import *
from database import *
from utils import *
from webhook import *

@accounts.route(f'{BASE_URL}/database/accounts/syncGJAccountNew.php', methods=['POST', 'GET'], strict_slashes=False)
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
    
    with open(f'../../data/account/{accountId}.gdacc') as f:
        save_data = f.read()
        
    return save_data + ";21;30;a;a"