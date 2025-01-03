import asyncio
import aiohttp
from typing import Optional, cast, Union
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
    """
    Класс для парсинга данных из поиска steam
    """
    def __init__(self) -> None:
        self._search_parser = SearchPageParser()
        self._game_parser = GamePageParser()

    @staticmethod
    def _prepare_url(languages: Union[list[str], None],
                    max_price: Union[int, str, None],
                    hide_free_to_play: bool) -> "SteamUrlConstructor":
        """
        Готовит url на основе переданных параметров с помощью класса SteamUrlConstructor
        """
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
        """
        Выполняет парсинг всех игр и их страниц для определенной страницы с играми из поиска
        """
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
                    hide_free_to_play: bool = False,
                    add_to_url: str = "",
                    languages: Optional[list[str]] = None,
                    max_price: Optional[int | str] = None,
                    ) -> list[
        dict[str, Any]
    ]:
        """Асинхронный метод для парсинга игр из Steam.

         Выполняет асинхронный парсинг страницы для поиска игр в Steam с учетом фильтров.
         Открывает новую aiohttp сессию для выполнения запросов.

         Parameters
         ----------
         num_pages : int
             Количество страниц для парсинга (на одной странице 25 игр).
         languages : Optional[list[str]]
             Список поддерживаемых языков для игр. Возможные значения получаются из метода `get_supported_lang`.
         max_price : Optional[int | str]
             Максимальная цена игры. Может быть целым числом или 'free'.
         hide_free_to_play : Optional[bool]
             Флаг для скрытия бесплатных игр.
         add_to_url : Optional[str]
             Строка, которая будет добавлена к сформированному URL.

         Returns
         -------
         list[dict]
             Список словарей с информацией о играх. Каждый словарь содержит следующие поля:
             - title : str
                 Название игры.
             - link : str
                 Ссылка на игру.
             - release_date : str
                 Дата выпуска игры.
             - final_price : float
                 Итоговая цена.
             - original_price : float
                 Изначальная цена (если была).
             - review_score : str
                 Оценка игры текстом.
             - positive_percentage : int
                 Процент положительных отзывов.
             - num_rev : int
                 Количество отзывов.
             - platforms : list[str]
                 Список платформ, на которых поддерживается игра.
             - developer : list[str]
                 Список разработчиков.
             - developer_link : list[str]
                 Список ссылок на страницы разработчиков.
             - publisher : list[str]
                 Список издателей.
             - publisher_link : list[str]
                 Список ссылок на страницы издателей.
             - tags : list[str]
                 Список категорий, к которым принадлежит игра.
         """
        session = await self.prepare_session()

        try:
            url = self._prepare_url(
                languages=languages,
                max_price=max_price,
                hide_free_to_play=hide_free_to_play
            )

            heap: heap_type = []

            tasks = [self._process_parse(
                url=url.add_page(i).url + add_to_url,
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
        """Возвращает список поддерживаемых языков для фильтрации игр в Steam.

        Данная функция использует метод `get_supported_lang` из класса `SteamUrlConstructor`
        для получения списка языков, которые поддерживаются Steam для фильтрации игр.

        Returns:
            list[str]: Список строк, где каждая строка представляет собой название языка
        """
        return SteamUrlConstructor().get_supported_lang()

