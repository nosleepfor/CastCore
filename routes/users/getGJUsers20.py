from . import users
from config import BASE_URL
from utils import *
from flask import request
from database import *

@users.route(f'{BASE_URL}/getGJUsers20.php', methods=['POST', 'GET'], strict_slashes=False)
def getGJUsers20():
    string = request.form.get('str')
    
    
    dict_cursor.execute('SELECT * FROM accounts WHERE username LIKE %s', (f'%{string}%',))
    users = dict_cursor.fetchall()
    
    
    users_str = ""
    
    if len(users) == 0:
        return '-1'
    
    for user in users:
        ao = user
        users_str += f"""1:{ao['username']}:2:{ao['id']}:13:{ao['coins']}:17:{ao['user_coins']}:6::9:{ao['icon_id']}:10:{ao['first_color']}:11:{ao['second_color']}:14:{ao['icon_type']}:15:0:16:{ao['id']}:3:{ao['stars']}:8:{ao['cp']}:4:{ao['demons']}|"""
        
    
    return users_str.removesuffix('|')+'#999:0:10'