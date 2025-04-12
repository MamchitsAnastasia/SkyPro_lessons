import pytest

from src import generators


@pytest.mark.parametrize(
    "currency_code, expected_count",
    [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0),
    ],
)
def test_filter_by_currency(sample_transactions, currency_code, expected_count):
    """Тестирует функцию filter_by_currency на корректное количество транзакций с заданной валютой."""
    filtered_transactions = list(generators.filter_by_currency(sample_transactions, currency_code))
    assert len(filtered_transactions) == expected_count
    for transaction in filtered_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == currency_code


def test_filter_by_currency_empty(empty_transactions):
    """Тестирует функцию filter_by_currency с пустым списком транзакций. Ожидается исключение ValueError."""
    with pytest.raises(ValueError):
        next(generators.filter_by_currency(empty_transactions, "USD"))


def test_filter_by_currency_invalid_input():
    """Тестирует функцию filter_by_currency с некорректными входными данными. Ожидается исключение TypeError."""
    with pytest.raises(TypeError):
        next(generators.filter_by_currency("not_a_list", "USD"))
    with pytest.raises(TypeError):
        next(generators.filter_by_currency([{"id": 1}], 123))


@pytest.mark.parametrize(
    "index, expected_description",
    [
        (0, "Перевод организации"),
        (1, "Перевод со счета на счет"),
        (2, "Перевод со счета на счет"),
        (3, "Перевод с карты на карту"),
        (4, "Перевод организации"),
    ],
)
def test_transaction_descriptions(sample_transactions, index, expected_description):
    """Тестирует функцию transaction_descriptions на корректное возвращение описаний транзакций."""
    descriptions = list(generators.transaction_descriptions(sample_transactions))
    assert descriptions[index] == expected_description


def test_transaction_descriptions_empty(empty_transactions):
    """Тестирует функцию transaction_descriptions с пустым списком транзакций. Ожидается исключение ValueError."""
    with pytest.raises(ValueError):
        next(generators.transaction_descriptions(empty_transactions))


def test_transaction_descriptions_invalid_input():
    """Тестирует функцию transaction_descriptions с некорректными входными данными.Ожидается исключение TypeError."""
    with pytest.raises(TypeError):
        next(generators.transaction_descriptions("not_a_list"))


@pytest.mark.parametrize(
    "start, end, expected_first, expected_last",
    [
        (1, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        (9999999999999995, 9999999999999999, "9999 9999 9999 9995", "9999 9999 9999 9999"),
        (1234, 1236, "0000 0000 0000 1234", "0000 0000 0000 1236"),
    ],
)
def test_card_number_generator(start, end, expected_first, expected_last):
    """Тестирует функцию card_number_generator на корректную генерацию номеров карт в заданном диапазоне."""
    generated_numbers = list(generators.card_number_generator(start, end))
    assert generated_numbers[0] == expected_first
    assert generated_numbers[-1] == expected_last
    assert len(generated_numbers) == end - start + 1


def test_card_number_generator_invalid_input():
    """Тестирует функцию card_number_generator с некорректными входными данными. Ожидается исключение TypeError или ValueError."""
    with pytest.raises(TypeError):
        next(generators.card_number_generator("1", 10))
    with pytest.raises(ValueError):
        next(generators.card_number_generator(-1, 10))
    with pytest.raises(ValueError):
        next(generators.card_number_generator(10, 10000000000000000))
    with pytest.raises(ValueError):
        next(generators.card_number_generator(10, 5))
