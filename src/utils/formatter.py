from decimal import Decimal

def vnd_format(value: int | float | Decimal) -> str:
    return "{:,.0f}".format(value).replace(',', '.')

