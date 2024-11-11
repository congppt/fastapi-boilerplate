from bcrypt import hashpw, gensalt, checkpw
from cryptography.fernet import Fernet

from constants.env import ENCRYPT_KEY


def hash_str(value: str) -> bytes:
    return hashpw(value.encode(), gensalt())

def match_original(target: str, source: bytes) -> bool:
    return checkpw(target.encode(), source)

__fernet = Fernet(ENCRYPT_KEY)

def encrypt(origin: str) -> bytes:
    return __fernet.encrypt(origin.encode())

def decrypt(encrypted: str) -> bytes:
    return __fernet.decrypt(encrypted.encode())
