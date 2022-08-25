import bcrypt
from app import db
from app.models import User

def generate_hash(password):
    # return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed    

def user_susume():
    pass
