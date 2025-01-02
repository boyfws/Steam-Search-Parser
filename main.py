import asyncio
import aiohttp
from typing import Optional
import heapq

from src import *

heap_type = list[
    tuple[
        int, list[dict[str,str | list[str]]]
    ]
]
class SteamParser(ValidateSteamData):
    def __init__(self):
        self.session = None
        self._search_parser = SearchPageParser()
        self._game_parser = GamePageParser()

    async def _process_parse(self,
                             url: str,
                             index: int,
                             heap: heap_type) -> None:
        html_parser = AsyncHTMLFetcher(session=self.session)

        async with html_parser.set_url(url) as search_html:
            games_list = self._search_parser.parse(search_html)

            for i in range(len(games_list)):

                async with html_parser.set_url(games_list[i]["link"]) as game_html:
                    extra_data = self._game_parser.parse(game_html)
                    games_list[i].update(extra_data)

        heapq.heappush(heap, (index, games_list))

    async def parse(self,
                    num_pages: int,
                    languages: Optional[list[str]] = None,
                    max_price: Optional[int | str] = None) -> list[
        dict[str, str | list[str]]
    ]:
        self.session = aiohttp.ClientSession()

        # Прокидываем куки, чтобы избежать показа страницы с выбором возраста
        self.session.cookie_jar.update_cookies({'birthtime': '283993201', 'mature_content': '1'})

        try:
            url = SteamUrlConstructor()

            if languages is not None:
                url.add_languages(languages)

            if max_price is not None:
                url.add_max_price(max_price)

            heap: heap_type = []

            tasks = [self._process_parse(
                url=url.add_page(i).url,
                index=i,
                heap=heap
            ) for i in range(1, num_pages + 1)]
            await asyncio.gather(*tasks)

        finally:
            await self.session.close()

        ret_array = []
        while heap:
            _, result = heapq.heappop(heap)
            ret_array += result

        return self._validate_data(data=ret_array)
