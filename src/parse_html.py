import aiohttp
from .logger import logger


class AsyncHTMLFetcher:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session
        self._url = None

    def set_url(self, url: str) -> "AsyncHTMLFetcher":
        self._url = url
        return self

    async def __aenter__(self) -> str:
        if self._url is None:
            raise ValueError("Не передан URL для возврата HTML")
        try:

            async with self.session.get(self._url) as response:
                return await response.text()

        except aiohttp.ClientError as e:
            error_type = type(e).__name__
            error_message = str(e)
            url = self._url
            logger.error(f"Возникла ошибка при получении html по url: {url} - {error_type}: {error_message}")

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        return False