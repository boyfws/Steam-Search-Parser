from bs4 import BeautifulSoup
import bs4


class SteamSearchPageHtmlParser:
    @staticmethod
    def _extract_data(game: bs4.Tag) -> dict[str, str | list[str]]:
        game_data = {
            "link": game['href'],
        }

        title = game.find('span', class_="title")
        if title:
            game_data["title"] = title.text.strip()

        release_date = game.find('div', class_='search_released')
        if release_date:
            game_data["release_date"] = release_date.text.strip()

        original_price = game.find('div', class_='discount_original_price')
        if original_price:
            game_data["original_price"] = original_price.text.strip()

        final_price = game.find('div', class_='discount_final_price')
        if final_price:
            game_data["final_price"] = final_price.text.strip()

        review_score = game.find('span', class_='search_review_summary')
        if review_score:
            game_data["review_score"] = review_score['data-tooltip-html']

        platforms = game.find_all('span', class_='platform_img')
        game_data["platforms"] = [platform['class'][1] for platform in platforms]  # win, mac, linux
        return game_data

    def parse(self, data: str) -> list[
        dict[str, list[str] | str]
    ]:
        """
        Обрабатывает данные со страницы с поиском
        """
        soup = BeautifulSoup(data, 'html.parser')
        game_rows = soup.find_all('a', class_='search_result_row')

        return [self._extract_data(el) for el in game_rows]