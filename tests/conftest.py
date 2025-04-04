from datetime import date, timedelta
from random import choice, randint
from typing import Callable, Optional

import pytest


# Фикстура для генерации случайных номеров карт
@pytest.fixture(scope="session")
def generate_random_card_number() -> Callable[[int], str]:
    def card_number_generate(length: int = 16) -> str:
        return "01" + "".join(str(randint(0, 9)) for _ in range(length - 2))

    return card_number_generate


# Фикстура для генерации случайных номеров счетов
@pytest.fixture(scope="session")
def generate_random_account_id() -> Callable[[int], str]:
    def account_id_generate(length: int = 20) -> str:
        return "01" + "".join(str(randint(0, 9)) for _ in range(length - 2))

    return account_id_generate


# Фикстура для генерации случайных наименований карт/счетов
@pytest.fixture(scope="session")
def generate_random_account_card_name() -> Callable[[Optional[str], Optional[int]], str]:
    types = ["Счет", "Карта"]
    lengths = [16, 20]

    def random_account_card_name_generate(type: Optional[str] = None, length: Optional[int] = None) -> str:
        if not type:
            type = choice(types)
        if not length:
            length = choice(lengths)

        name = type + " " + "".join(str(randint(0, 9)) for _ in range(length))
        return name

    return random_account_card_name_generate


# Фикстура для генерации случайных дат
@pytest.fixture(scope="session")
def generate_random_date() -> str:
    today = date.today()
    days_ago = randint(-365, 365)
    random_date = today + timedelta(days=days_ago)
    formated_random_date = random_date.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return formated_random_date
