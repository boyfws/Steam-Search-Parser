import aiohttp


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

        response = await self.session.get(self._url)
        try:
            return await response.text()
        finally:
            response.close()  # Закрываем response

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        return False