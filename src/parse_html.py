import aiohttp
from types import TracebackType
from typing import Optional, Type, TypeVar

from .logger import logger

_ExcType = TypeVar('_ExcType', bound=BaseException)


class AsyncHTMLFetcher:
    _url: None | str
    session: aiohttp.ClientSession

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session
        self._url = None

    def set_url(self, url: str) -> "AsyncHTMLFetcher":
        self._url = url
        return self

    async def __aenter__(self) -> str | None:
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
            return None

    async def __aexit__(
            self,
            exc_type: Optional[Type[_ExcType]],
            exc_val: Optional[_ExcType],
            exc_tb: Optional[TracebackType]
    ) -> bool:
        return False