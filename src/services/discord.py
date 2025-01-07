from httpx import AsyncClient

from config import APP_SETTINGS
from constants import REQUEST_TIMEOUT

__CONFIG = APP_SETTINGS.discord
__CLIENT = AsyncClient(base_url=__CONFIG.base_url, timeout=REQUEST_TIMEOUT, proxy=APP_SETTINGS.proxy, verify=False)
async def asend_notification(message: str):
    """Send notification to Discord"""
    await __CLIENT.post(url=__CONFIG.notification_path, data={"content": message[:2000]})
