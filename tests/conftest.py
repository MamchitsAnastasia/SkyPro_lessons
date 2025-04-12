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


# "Фикстура с примером списка транзакций для тестирования
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


# Фикстура с пустым списком транзакций
@pytest.fixture
def empty_transactions():
    return []
