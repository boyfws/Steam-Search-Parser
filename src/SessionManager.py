import aiohttp


class SessionManager:
    """
    Класс для открытия сессии внутри парсера
    """
    # Добавляем await так как сессия может создаваться только внутри event loop - а
    @staticmethod
    async def prepare_session() -> aiohttp.ClientSession:
        """
        Метод открывающий сессию - может быть использован для интеграции rate limiter-а
        """
        session = aiohttp.ClientSession()

        # Прокидываем куки, чтобы избежать показа страницы с выбором возраста
        session.cookie_jar.update_cookies({'birthtime': '283993201', 'mature_content': '1'})

        return session
