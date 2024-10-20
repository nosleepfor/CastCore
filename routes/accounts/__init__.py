from flask import Blueprint

accounts = Blueprint('accounts', __name__)

from .backupGJAccountNew import *
from .loginGJAccount import *
from .registerGJAccount import *
from .syncGJAccountNew import *