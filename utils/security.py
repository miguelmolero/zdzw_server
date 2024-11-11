from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str):
    return ph.hash(password)

def verify_password(password: str, hashed_password: str):
    try:
        return ph.verify(hashed_password, password)
    except Exception as e:
        print("Invalid password", e)
        return False