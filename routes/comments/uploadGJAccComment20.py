from . import comments
from flask import request
from config import *
from database import *

@comments.route(f"{BASE_URL}/uploadGJAccComment20.php", methods=['POST'], strict_slashes=False)
def uploadGJAccComment20():
    accountId = request.form.get('accountID')
    comment = request.form.get('comment')
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
    
    cursor.execute('INSERT INTO accComments (text, likes, author_id, upload_time) VALUES (%s, %s, %s, %s)', (comment, 0, accountId, time.time()))
    
    cursor.execute('SELECT LAST_INSERT_ID()')
    comment_id = cursor.fetchone()[0]
    
    return str(comment_id)