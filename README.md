# Steam Search Parser
Данный проект предоставляет класс `SteamParser` для парсинга данных об играх из поиска Steam.
## Методы

```python 
   parse(
    num_pages: int, 
    languages: Optional[list[str]] = None, 
    max_price: Optional[int | str] = None, 
    hide_free_to_play: Optional[bool] = False, 
    add_to_url: Optional[str] = ""
        ) -> list[dict[str, Any]]
```
Асинхронный метод для парсинга игр из Steam.

Полученные данные валидируются с помощью pydantic: 
```python
class ResponseFormat(BaseModel):
    title: str
    link: str
    release_date: date
    final_price: float
    original_price: Optional[float] = None

    review_score: str
    positive_percentage: int
    num_rev: int

    platforms: list[str]

    developer: list[str]
    developer_link: list[str]
    publisher: Optional[list[str]] = None
    publisher_link: Optional[list[str]] = None

    tags: list[str]
```


**Параметры:**
- `num_pages`: Количество страниц для парсинга (на одной странице 25 игр).
- `languages`: Список поддерживаемых языков для игр. Возможные значения можно получить с помощью метода `get_supported_lang`.
- `max_price`: Максимальная цена игры. Может быть целым числом или строкой `'free'`.
- `hide_free_to_play`: Флаг для скрытия бесплатных игр. По умолчанию `False`.
- `add_to_url`: Дополнительная строка, которая будет добавлена к сформированному URL. По умолчанию пустая строка.

**Возвращает:**
- `list[dict]`: Список словарей с информацией о играх. Каждый словарь содержит следующие поля:
  - `title`: Название игры.
  - `link`: Ссылка на игру.
  - `release_date`: Дата выпуска игры.
  - `final_price`: Итоговая цена.
  - `original_price`: Изначальная цена (если была).
  - `review_score`: Оценка игры текстом.
  - `positive_percentage`: Процент положительных отзывов.
  - `num_rev`: Количество отзывов.
  - `platforms`: Список платформ, на которых поддерживается игра.
  - `developer`: Список разработчиков.
  - `developer_link`: Список ссылок на страницы разработчиков.
  - `publisher`: Список издателей.
  - `publisher_link`: Список ссылок на страницы издателей.
  - `tags`: Список категорий, к которым принадлежит игра.
