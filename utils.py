import hashlib
import bcrypt

salt = "mI29fmAnxgTs"

def hash_passw(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('ascii')

def gen_gjp2(password, bcrypt=False):
    hash = hashlib.sha1()
    hash.update((password + salt).encode())
    gjp2 = hash.hexdigest()
    return gjp2