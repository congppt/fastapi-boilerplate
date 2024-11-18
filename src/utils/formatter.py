from decimal import Decimal

def vnd_format(value: int | float | Decimal) -> str:
    """
    Format number to VNĐ style
    :param value: number to format
    :return: VNĐ style representation of given number
    """
    return "{:,.0f}".format(value).replace(',', '.')

