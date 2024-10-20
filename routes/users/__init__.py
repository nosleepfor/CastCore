from flask import Blueprint

users = Blueprint('users', __name__)

from .getGJUserInfo import *
from .getGJUsers20 import *
from .updateGJUserScore22 import *