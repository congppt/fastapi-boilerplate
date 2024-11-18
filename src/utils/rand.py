import random
import string



def random_otp(length: int) -> str:
    # noinspection PyTypeChecker
    return ''.join(random.choices(string.digits, k=length))

def random_str(length: int) -> str:
    # noinspection PyTypeChecker
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))