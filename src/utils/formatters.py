import os
import traceback
from decimal import Decimal
from traceback import StackSummary
from typing import Literal

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

def format_exception(e: Exception, extract: Literal['trace', 'stack'] = 'trace'):
    frames: StackSummary = StackSummary()
    if extract == 'trace':
        frames = traceback.extract_tb(e.__traceback__)
    else:
        frames = traceback.extract_stack(e.__traceback__)
    non_lib_frames = [frame for frame in frames
                      if 'site-packages' not in frame.filename
                      and 'lib' not in frame.filename]
    last_frame = non_lib_frames[-1] if non_lib_frames else frames[-1]
    return f"\n**Traceback**: {last_frame}\n**Exception**: {e}\n"
