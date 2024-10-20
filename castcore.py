import time, colorama
from flask import Flask, request
import hashlib
from database import *
from webhook import send_webhook
from utils import *
from config import *
import urllib

from routes.users import users
from routes.comments import comments
from routes.accounts import accounts
from routes.misc import misc

VERSION = '0.1'

colorama.init()
app = Flask(__name__)

app.register_blueprint(users)
app.register_blueprint(comments)
app.register_blueprint(accounts)

@app.route(f"{BASE_URL}/getAccountURL.php", methods=['POST', 'GET'], strict_slashes=False)
def getAccountURL():
    return 'http://localhost:5000/gdps/datagds'


print(f'CastCore - {VERSION} Running! [{time.strftime("%H:%M:%S")}]\n{colorama.Fore.GREEN}Made specifically for the FDPS project.{colorama.Fore.RESET}')
