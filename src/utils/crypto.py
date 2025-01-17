from bcrypt import hashpw, gensalt, checkpw
from cryptography.fernet import Fernet

from config import APP_SETTINGS


def hash_str(value: str | bytes, to_str=False):
    """
    Hash original string/bytes
    :param value: original string
    :param to_str: return string(True) or bytes(False) (default: False)
    :return: Hashed bytes
    """
    value = value.encode() if isinstance(value, str) else value
    result = hashpw(password=value, salt=gensalt())
    return result.decode() if to_str else result


def match_original(target: str | bytes, source: bytes):
    """
    Check if given string is origin of hashed bytes
    :param target: given string/bytes
    :param source: hashed bytes
    :return: True if given string is origin of hashed bytes
    """
    target = target.encode() if isinstance(target, str) else target
    return checkpw(password=target, hashed_password=source)


__fernet = Fernet(key=APP_SETTINGS.encrypt_key)


def encrypt(origin: str | bytes, to_str=False):
    """
    Encrypt given string to bytes
    :param origin: original string
    :param to_str: return string(True) or bytes(False) (default: False)
    :return: encrypted string/bytes
    """
    origin = origin.encode() if isinstance(origin, str) else origin
    result = __fernet.encrypt(data=origin)
    return result.decode() if to_str else result


def decrypt(encrypted: str | bytes, to_str=True):
    """
    Decrypt given string to original bytes
    :param encrypted: encrypted string
    :param to_str: return string(True) or bytes(False) (default: True)
    :return: decrypted string/bytes
    """
    encrypted = encrypted.encode() if isinstance(encrypted, str) else encrypted
    result = __fernet.decrypt(token=encrypted)
    return result.decode() if to_str else result
