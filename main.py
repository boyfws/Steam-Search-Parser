import asyncio
import aiohttp
from typing import Optional

from src import *


class SteamParser:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

        self._search_parser = SearchPageParser()
        self._game_parser = GamePageParser()

    async def _process_parse(self,
                             url: str,
                             index: int,
                             queue: asyncio.Queue) -> None:
        html_parser = AsyncHTMLFetcher(session=self.session)

        async with html_parser.set_url(url) as search_html:
            games_list = self._search_parser.parse(search_html)

            for i in range(len(games_list)):

                async with html_parser.set_url(games_list[i]["link"]) as game_html:
                    extra_data = self._game_parser.parse(game_html)
                    games_list[i].update(extra_data)

        await queue.put((index, games_list))

    async def parse(self, num_pages: int, languages: Optional[list[str]] = None, max_price: Optional[int | str] = None) -> list[
        dict[str, str | list[str]]
    ]:
        url = SteamUrlConstructor()

        if languages is not None:
            url.add_languages(languages)

        if max_price is not None:
            url.add_max_price(max_price)

        queue = asyncio.Queue()
        tasks = [self._process_parse(
            url=url.add_page(i).url,
            index=i,
            queue=queue
        ) for i in range(1, num_pages + 1)]
        await asyncio.gather(*tasks)

        results = []
        while not queue.empty():
            index, result = await queue.get()
            results.append((index, result))

        ret_array = []
        for _, result in sorted(results, key=lambda x: x[0]):
            ret_array += result

        return ret_array
