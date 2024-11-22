from http import HTTPMethod


from config import STARTUP_CONFIG
from config.schema import DiscordConfig
from constants import REQUEST_TIMEOUT
from constants.env import PROXY
from utils.http_client import HTTPClient

__CONFIG: DiscordConfig = STARTUP_CONFIG.get(section='discord', model=DiscordConfig)
__CLIENT = HTTPClient(base_url=__CONFIG.base_url, timeout=REQUEST_TIMEOUT, proxy=PROXY, verify=False)
async def asend_notification(message: str) -> None:
    """Send notification to Discord"""
    print(HTTPMethod.POST)
    request = __CLIENT.build_request(method=HTTPMethod.POST, url=__CONFIG.notification_path, data={"content": message[:2000]})
    response = await __CLIENT.asend(request)
    print(response)
