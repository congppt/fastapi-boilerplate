import os
import traceback
from decimal import Decimal

from starlette.templating import Jinja2Templates


def format_vnd(value: int | float | Decimal):
    """
    Format number to VNĐ style
    :param value: number to format
    :return: VNĐ style representation of given number
    """
    return "{:,.0f}".format(value).replace(",", ".")


async def aformat_html(
    file_path: str, filler: dict[str, str | int | float] | None = None
):
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


def format_exception(e: Exception):
    # Extract the complete traceback as a list of FrameSummary objects
    frames = traceback.extract_tb(tb=e.__traceback__)
    # Define which paths we consider "library" code:
    # Adjust these patterns to match your environment or preferences
    # (e.g., "/usr/local/lib/python3.", "site-packages", etc.)
    excluded_paths = {
        os.path.join(os.path.sep, "usr", "lib", "python3"),
        os.path.join(os.path.sep, "Library", "Python"),
        "site-packages",
    }
    # Filter out frames whose `filename` starts with or contains library paths
    filtered_frames = []
    for frame in frames:
        # If the filename does not match any of our excluded paths, keep it
        if not any(path_fragment in frame.filename for path_fragment in excluded_paths):
            filtered_frames.append(frame)
    last_frame = filtered_frames[-1] if filtered_frames else frames[-1]
    return (
        f"\n**Traceback**:{frames.format_frame_summary(last_frame)}**Exception**: {e}"
    )
