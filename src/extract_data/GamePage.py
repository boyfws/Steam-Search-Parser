from bs4 import BeautifulSoup
import bs4


class SteamGamePageHtmlParser:
    @staticmethod
    def _extract_dev_pub(soup: bs4.BeautifulSoup) -> dict[str, list[str]]:
        result_dict = {}

        dev_rows = soup.find_all('div', **{"class": "dev_row"})

        for row in dev_rows:
            try:
                subtitle = row.find('div', **{"class": "subtitle column"}).text.strip()
                summary = row.find('div', **{"class": "summary column"}).text.strip()
                link_tag = row.find('a')

                if link_tag is None:
                    continue

                try:
                    link = link_tag['href']
                except KeyError:
                    link = ""

                if subtitle == "Developer:":
                    result_dict["developer"] = result_dict.get("developer", []) + [summary]
                    result_dict["developer_link"] = result_dict.get("developer_link", []) + [link]

                if subtitle == "Publisher:":
                    result_dict["publisher"] = result_dict.get("publisher", []) + [summary]
                    result_dict["publisher_link"] = result_dict.get("publisher_link", []) + [link]

            except AttributeError:
                continue

        return result_dict

    @staticmethod
    def _extract_tags(soup: bs4.BeautifulSoup) -> dict[str, list[str]]:
        tags = soup.find_all('a', class_='app_tag')

        tag_names = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True) != "+"]

        return {"tags": tag_names}

    def parse(self, data: str) -> dict[
        str, str | list[str]
    ]:
        result_dict = {}
        soup = BeautifulSoup(data, 'html.parser')

        result_dict.update(self._extract_dev_pub(soup))
        result_dict.update(self._extract_tags(soup))

        return result_dict
