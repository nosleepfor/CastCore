from flask import Blueprint

comments = Blueprint('comments', __name__)

from .getGJAccountComments20 import *
from .uploadGJAccComment20 import *