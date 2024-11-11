from http import HTTPMethod

from httpx import Request

from src.constants.env import PROXY
from src.constants.external import Discord, REQUEST_TIMEOUT
from src.utils.http_client import HTTPClient

__DISCORD = HTTPClient(base_url=Discord.DISCORD_BASE, timeout=REQUEST_TIMEOUT, proxy=PROXY, verify=False)

async def asend_notification(message: str) -> None:
    """Send notification to Discord"""
    request = Request(method=HTTPMethod.POST, url=Discord.NOTIFICATION_PATH, data = {"content": message[:2000]})
    await __DISCORD.asend(request)
