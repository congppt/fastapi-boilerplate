import random
import string


def random_otp(length: int):
    """
    Randomize OTP (digits only)
    :param length: length of output OTP
    :return: random otp
    """
    # noinspection PyTypeChecker
    return "".join(random.choices(population=string.digits, k=length))


def random_str(length: int):
    """
    Randomize a string (Alphabet + digits)
    :param length: length of output string
    :return: random string
    """
    # noinspection PyTypeChecker
    return "".join(random.choices(population=string.ascii_letters + string.digits, k=length))
