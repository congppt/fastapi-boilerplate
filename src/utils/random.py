import random
import string


def random_otp(length: int) -> str:
    """
    Randomize OTP (digits only)
    :param length: length of output OTP
    :return: random otp
    """
    # noinspection PyTypeChecker
    return ''.join(random.choices(string.digits, k=length))


def random_str(length: int) -> str:
    """
    Randomize a string (Alphabet + digits)
    :param length: length of output string
    :return: random string
    """
    # noinspection PyTypeChecker
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
