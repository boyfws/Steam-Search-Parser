class SteamUrlParamManager:
    @staticmethod
    def _add_lang_to_url(lang_params: list[str]) -> str:
        lang_string = ""
        lang_string += "&supportedlang="
        lang_string += "%".join(lang_params)
        return lang_string

    @staticmethod
    def _add_page_to_url(page: int) -> str:
        page_string = ""
        page_string += f"&page={page}"
        return page_string

    @staticmethod
    def _add_max_price_to_url(max_price: int | str) -> str:
        max_price_string = ""
        max_price_string += f"&maxprice={max_price}"
        return max_price_string

    @staticmethod
    def _add_32play_flag() -> str:
        return "&hidef2p=1"
