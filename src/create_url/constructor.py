from .lang_param import SupportedLangParam
from .param_manager import SteamUrlParamManager


class SteamUrlConstructor(SteamUrlParamManager):
    @staticmethod
    def _prepare_base_url(base_url: str) -> str:
        base_url += "filter=popularnew"
        base_url += "&ndl=1"
        base_url += "&ignore_preferences=1"
        return base_url

    def __init__(self):
        self._url = self._prepare_base_url("https://store.steampowered.com/search/?")

        self._lang_converter = SupportedLangParam()
        self._lang = self._lang_converter.convert_lang(["русский"])

        self._page = -1

        self._max_price = -1

    def add_languages(self, lang: list[str]) -> "SteamUrlConstructor":
        """
        Добавление языка в ссылку
        """
        list_of_lang = self._lang_converter.convert_lang(lang)
        self._lang += [el for el in list_of_lang if el not in self._lang]
        return self

    def add_page(self, page_num: int) -> "SteamUrlConstructor":
        """
        Добавление страницы в ссылку
        """
        if not isinstance(page_num, int):
            raise ValueError("Номер страницы должна иметь тип int")

        if page_num <= 0:
            raise ValueError("Номер страницы не может быть меньше 1")

        self._page = page_num
        return self

    def add_max_price(self, max_price: int | str) -> "SteamUrlConstructor":
        """
        Добавляет max_price в URL,
        :param max_price: либо str 'free' либо int
        """
        if isinstance(max_price, str):
            if max_price == "free":
                self._max_price = "free"
                return self
            else:
                raise ValueError("Если макс цена передана как str то она может принимать только значение free")

        if not isinstance(max_price, int):
            raise ValueError("Максимальная цена иметь тип int")

        if max_price <= 0:
            raise ValueError("Максимальная цена не может быть меньше 0")

        av_values = [150, 300, 450, 600, 750, 900, 1050, 1200, 1350, 1500, 1650, 1800]

        if max_price not in av_values:
            raise ValueError(f"Steam поддерживает список из следующих максимальных цен: {av_values}")

        self._max_price = max_price

        return self

    @property
    def url(self) -> str:
        """
        Производит сборку URL-a
        """
        url = self._url

        if self._page != -1:
            url += self._add_page_to_url(self._page)

        if len(self._lang) != 0:
            url += self._add_lang_to_url(self._lang)

        if self._max_price != -1:
            url += self._add_max_price_to_url(self._max_price)

        return url