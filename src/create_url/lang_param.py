class SupportedLangParam:
    """
    Отвечает за конвертацию языков в URL
    """
    def __init__(self) -> None:
        self._conv_dict = {
            "русский": "russian",
            "китайский (упр.)": "2Cschinese",
            "китайский (трад.)": "2Ctchinese",
            "японский": "2Cjapanese",
            "корейский": "2Ckoreana",
            "тайский": "2Cthai",
            "болгарский": "2Cbulgarian",
            "чешский": "2Cczech",
            "датский": "2Cdanish",
            "немецкий": "2Cgerman",
            "английский": "2Cenglish",
            "испанский": "2Cspanish",
            "испанский (латиноам.)": "2Clatam",
            "греческий": "2Cgreek",
            "французский": "2Cfrench"
        }

    def get_supported_lang(self) -> list[str]:
        """
        Возвращает список доступных языков
        """
        return list(self._conv_dict.keys())

    def convert_lang(self, languages: list[str]) -> list[str]:
        """
        Конвертирует список языков в список параметров
        """
        try:
            return [self._conv_dict[el] for el in languages]
        except KeyError:
            raise KeyError("Использован неподдерживаемый язык")