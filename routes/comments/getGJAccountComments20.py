from flask import request
from . import comments
from config import *
from database import *

@comments.route(f"{BASE_URL}/getGJAccountComments20.php", methods=['POST', 'GET'], strict_slashes=False)
def getGJAccountComments20():
    accountID = request.values.getlist('accountID')[1]
    print([s for s in request.form.items()])

    dict_cursor.execute("SELECT * FROM accComments WHERE author_id = %s ORDER BY id DESC", (accountID,))
    comments = dict_cursor.fetchall()
    
    comments_str = ""
    for comment in comments:
        comments_str += f"2~{comment['text']}~4~{comment['likes']}~6~{comment['id']}~9~{time_conv(comment['upload_time'])}|"
    print(comments_str)
    return comments_str.removesuffix('|')+'#0:0:0'