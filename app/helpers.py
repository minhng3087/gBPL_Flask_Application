import bcrypt

def generate_hash(password):
    # return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed    