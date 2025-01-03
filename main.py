import asyncio
import aiohttp
from typing import Optional, cast
import heapq
from typing import Any

from src import (
    ValidateSteamData,
    SearchPageParser,
    GamePageParser,
    AsyncHTMLFetcher,
    SteamUrlConstructor,
    SessionManager
)


heap_type = list[
    tuple[
        int, list[dict[str,str | list[str]]]
    ]
]


class SteamParser(ValidateSteamData, SessionManager):
    def __init__(self) -> None:
        self._search_parser = SearchPageParser()
        self._game_parser = GamePageParser()

    @staticmethod
    def _prepare_url(languages: list[str],
                    max_price: int | str,
                    hide_free_to_play: bool) -> "SteamUrlConstructor":
        url = SteamUrlConstructor()

        url = url.add_hide_free_to_play(
            hide_free_to_play
        )

        if languages is not None:
            url.add_languages(languages)

        if max_price is not None:
            url.add_max_price(max_price)

        return url

    async def _process_parse(self,
                             url: str,
                             index: int,
                             heap: heap_type,
                             session: aiohttp.ClientSession) -> None:
        html_parser = AsyncHTMLFetcher(session=session)

        async with html_parser.set_url(url) as search_html:
            if search_html is None:
                return None

            games_list = self._search_parser.parse(search_html)

            for i in range(len(games_list)):

                link = cast(str, games_list[i]["link"])  # Приводим тип к str
                async with html_parser.set_url(link) as game_html:

                    if game_html is None:
                        continue

                    extra_data = self._game_parser.parse(game_html)
                    games_list[i].update(extra_data)

        heapq.heappush(heap, (index, games_list))

    async def parse(self,
                    num_pages: int,
                    languages: Optional[list[str]] = None,
                    max_price: Optional[int | str] = None,
                    hide_free_to_play: Optional[bool] = False) -> list[
        dict[str, Any]
    ]:
        session = await self.prepare_session()

        try:
            url = self._prepare_url(
                languages=languages,
                max_price=max_price,
                hide_free_to_play=hide_free_to_play
            )

            heap: heap_type = []

            tasks = [self._process_parse(
                url=url.add_page(i).url,
                index=i,
                heap=heap,
                session=session
            ) for i in range(1, num_pages + 1)]

            await asyncio.gather(*tasks)

        finally:
            await session.close()

        ret_array = []
        while heap:
            _, result = heapq.heappop(heap)
            ret_array += result

        return self._validate_data(data=ret_array)

    @staticmethod
    def get_supported_lang() -> list[str]:
        return SteamUrlConstructor().get_supported_lang()

