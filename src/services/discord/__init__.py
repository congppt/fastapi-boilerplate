from ssl import SSLContext

from httpx import AsyncClient

from config.schema import DiscordAPISettings
import logger


class DiscordAPI:
    def __init__(
        self,
        timeout: int,
        proxy: str | None,
        verify: SSLContext | str | bool,
        api: DiscordAPISettings,
    ):
        self._client = AsyncClient(
            base_url="https://discord.com/api/",
            timeout=timeout,
            proxy=proxy,
            verify=verify,
        )
        self._api = api

    async def asend_bot_message(self, message: str):
        """Send notification to Discord"""
        if not self._client:
            raise ValueError("Discord API client is not initialized")
        await self._client.post(url=self._api.chatbot, data={"content": message[:2000]})

    async def aclose(self):
        if not self._client:
            raise ValueError("Discord API client is not initialized")
        await self._client.aclose()
        self._client = None
        logger.log("Discord API client is closed")
