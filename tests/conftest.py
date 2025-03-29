import pytest
from datetime import date, timedelta
from random import choice, randint, sample
from string import ascii_uppercase, digits


# Фикстура для генерации случайных номеров карт
@pytest.fixture(scope="session")
def generate_random_card_number():
    def card_number_generate(length=16):
        return ''.join(str(randint(0, 9)) for _ in range(length))

    return card_number_generate


# Фикстура для генерации случайных номеров счетов
@pytest.fixture(scope="session")
def generate_random_account_id():
    def account_id_generate(length=20):
        return ''.join(str(randint(0, 9)) for _ in range(length))

    return account_id_generate


# Фикстура для генерации случайных наименований карт/счетов
@pytest.fixture(scope="session")
def generate_random_account_card_name():
    types = ["Счет", "Карта"]
    lengths = [20, 30]

    def _generate(type=None, length=None):
        if not type:
            type = choice(types)
        if not length:
            length = choice(lengths)

        name = type + '-' + ''.join(sample(digits, length))
        return name

    return _generate


# Фикстура для генерации случайных дат
@pytest.fixture(scope="session")
def generate_random_date():
    today = date.today()
    days_ago = randint(-365, 365)
    random_date = today + timedelta(days=days_ago)
    return random_date.strftime("%Y-%m-%d")


# Фикстура для генерации списка операций
@pytest.fixture(scope="session")
def generate_operations_list():
    states = ["EXECUTED", "PENDING", "FAILED"]
    dates = [date.today().strftime("%Y-%m-%d")]

    operations = []
    for i in range(10):
        operation = {
            "id": i,
            "name": f"Operation-{i}",
            "date": choice(dates),
            "state": choice(states),
            "amount": randint(100, 20000)
        }
        operations.append(operation)

    return operations