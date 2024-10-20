from flask import request
from . import misc
from config import *
from database import *
from utils import *


@misc.route(f'{BASE_URL}/likeGJItem211.php', methods=['POST', 'GET'], strict_slashes=False)
def likeGJItem211():
    accountId = int(request.form.get('accountID')) if request.form.get('accountID') else None
    if accountId:
        password = request.form.get('gjp')
        gjp = request.form.get('gjp2')

        is_gjp2 = False

        if gjp not in [None, '']:
            is_gjp2 = True
            password = gjp

        if accountId <= 0:
            return "1"
        
        user = get_account_by_id(accountId)
        
        if user[3] != password:
            return "1"
        
        type = request.form.get('type')
        itemId = int(request.form.get('itemID'))
        like = 1 if request.form.get('like') != 0 else -1
        
        cursor.execute('INSERT INTO likes (item_id, item_type, account_id, timestamp, ip) VALUES (%s, %s, %s, %s, %s)', (itemId, type, accountId, time.time(), request.remote_addr))
          
        if type == 3:
            cursor.execute('UPDATE accComments SET likes = likes + %s WHERE id = %s', (like, itemId))
            
        return "1"