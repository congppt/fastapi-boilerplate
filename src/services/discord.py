from ssl import SSLContext

from httpx import AsyncClient

import logger


class DiscordAPI:
    def __init__(
            self,
            base_url: str,
            timeout: int,
            proxy: str,
            verify: SSLContext | str | bool
    ):
        self._client = AsyncClient(
            base_url=base_url,
            timeout=timeout,
            proxy=proxy,
            verify=verify
        )

    async def asend_bot_message(self, message: str, chatbot_hook: str):
        """Send notification to Discord"""
        await self._client.post(url=chatbot_hook, data={"content": message[:2000]})

    async def aclose(self):
        await self._client.aclose()
        self._client = None
        logger.log("Discord API client is closed")