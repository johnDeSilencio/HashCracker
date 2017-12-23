import hashlib

def hash(string):
    return hashlib.sha256(string).hexdigest()

def isHash(passwordHash, guessHash):
    if passwordHash is guessHash:
        return True
    return False
