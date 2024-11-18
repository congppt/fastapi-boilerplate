import os
from decimal import Decimal

from starlette.templating import Jinja2Templates


def format_vnd(value: int | float | Decimal) -> str:
    """
    Format number to VNĐ style
    :param value: number to format
    :return: VNĐ style representation of given number
    """
    return "{:,.0f}".format(value).replace(',', '.')

async def aformat_html(file_path: str, filler: dict[str, str | int | float] = None) -> str:
    """
    Format html file as string and return its content
    :param file_path: html file path
    :param filler: data to fill in html file
    :return: html content as string
    """
    filler = filler or {}
    directory, filename = os.path.split(file_path)
    templates = Jinja2Templates(directory=directory, enable_async=True)
    template = templates.get_template(name=filename)
    return await template.render_async(filler)
