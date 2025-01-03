import aiohttp


class SessionManager:
    # Добавляем await так как сессия может создаваться только внутри event loop - а
    @staticmethod
    async def prepare_session() -> aiohttp.ClientSession:
        session = aiohttp.ClientSession()

        # Прокидываем куки, чтобы избежать показа страницы с выбором возраста
        session.cookie_jar.update_cookies({'birthtime': '283993201', 'mature_content': '1'})

        return session
