from . import accounts
from flask import request
from config import *
from database import *
from utils import *
from webhook import *

@accounts.route(f'{BASE_URL}/database/accounts/backupGJAccountNew.php', methods=['POST', 'GET'], strict_slashes=False)
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
    
    with open(f'../../data/account/{accountId}.gdacc', 'w') as f:
        f.write(save_data)
        
    return "1"