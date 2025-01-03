from .logger import logger

from pydantic import BaseModel, field_validator, ValidationError
from typing import Any
from datetime import datetime, date
from typing import Optional, Union


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

    @field_validator("final_price", "original_price", mode='before')
    def convert_price(cls, value: str) -> str:
        if value == "Free":
            return "0"

        return value.split()[0].replace(",", ".")

    @field_validator('release_date', mode='before')
    def parse_custom_date(cls, value: str) -> date | None:
        try:
            return datetime.strptime(value, "%d %b, %Y").date()
        except ValueError:
            pass

        # Пробуем второй формат: '%b %Y'
        try:
            return datetime.strptime(value, "%b %Y").date()
        except ValueError:
            return None

    @field_validator("positive_percentage", mode="before")
    def parse_percentage(cls, value: str) -> str:
        return value.rstrip("%")

    @field_validator("num_rev", mode="before")
    def parse_num_rev(cls, value: str) -> str:
        return value.replace(",", "")


class ValidateSteamData:
    """
    Класс-валидатор для полученных от парсера данных
    """
    @staticmethod
    def __extract_score(score: str) -> dict[str, str]:
        """
        Распаковывает строку с рейтингом игры
        """
        score_split = score.split("<br>")
        game_score = score_split[0].strip()
        positive_percentage = score_split[1].split(" ")[0].strip()
        num_rev = score_split[1].split(" ")[3]
        return {"review_score": game_score,
                "positive_percentage": positive_percentage,
                "num_rev": num_rev}

    @staticmethod
    def __conv_to_resp_format(
            el: dict[str, str | list[str]],
    ) -> Union["ResponseFormat", None]:
        """
        Преобразует один элемент возвращаемый парсером в ResponseFormat для валидации и
        конвертирует его в словарь
        """
        try:
            if isinstance(el["review_score"], list):
                return None

            el.update(
                ValidateSteamData.__extract_score(el["review_score"])
            )
            # Мы прокидываем ингор, так как функция данной строчки конвертация типов
            return ResponseFormat(**el)  # type: ignore

        except (ValidationError, KeyError) as e:
            logger.info(f"Произошла ошибка при валидации игры {el['title']} {el['link']}")
            return None

    @staticmethod
    def _validate_data(
            data: list[
                dict[str, str | list[str]]
            ],
            included_fields: Optional[list[str]] = None
    ) -> list[dict[str, Any]]:
        """
        Валидирует входные данные от парсера
        """
        ret_array_iter = (ValidateSteamData.__conv_to_resp_format(el) for el in data)

        included_fields_set = None
        if included_fields is not None:
            included_fields_set = set(included_fields)

        return [el.model_dump(include=included_fields_set) for el in ret_array_iter if el is not None]
