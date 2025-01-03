from bs4 import BeautifulSoup
import bs4
from ..logger import logger


class SteamGamePageHtmlParser:
    @staticmethod
    def _extract_dev_pub(soup: bs4.BeautifulSoup) -> dict[str, list[str]]:
        result_dict: dict[str, list[str]] = {}

        dev_rows = soup.find_all('div', class_="dev_row")

        for row in dev_rows:
            try:
                subtitle_obj = row.find('div', class_="subtitle column")

                if subtitle_obj is None:
                    continue

                subtitle = subtitle_obj.text
                summary = row.find('div', class_="summary column")

                if subtitle == "Developer:":
                    for link_tag in summary.find_all('a'):
                        result_dict["developer"] = result_dict.get("developer", []) + [link_tag.text.strip()]
                        result_dict["developer_link"] = result_dict.get("developer_link", []) + [link_tag['href']]

                elif subtitle == "Publisher:":
                    for link_tag in summary.find_all('a'):
                        result_dict["publisher"] = result_dict.get("publisher", []) + [link_tag.text.strip()]
                        result_dict["publisher_link"] = result_dict.get("publisher_link", []) + [link_tag['href']]

            except (AttributeError, KeyError) as e:
                continue

        return result_dict

    @staticmethod
    def _extract_tags(soup: bs4.BeautifulSoup) -> dict[str, list[str]]:
        tags = soup.find_all('a', class_='app_tag')
        try:
            tag_names = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True) != "+"]

        except AttributeError:
            logger.error("Возникла ошибка при извлечении категорий")
            return {}

        return {"tags": tag_names}

    def parse(self, data: str) -> dict[
        str, list[str]
    ]:
        result_dict = {}
        soup = BeautifulSoup(data, 'html.parser')

        result_dict.update(self._extract_dev_pub(soup))
        result_dict.update(self._extract_tags(soup))

        return result_dict
