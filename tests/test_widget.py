import pytest
import re
import datetime
from src import widget
from typing import Callable, List, Any, Optional

@pytest.mark.parametrize("account_card, expected_result",
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ],
)
def test_valid_account_card_name(account_card: str, expected_result: str) -> None:
    """Тестирует функцию с корректными номерами."""
    result = widget.mask_account_card(account_card)
    assert result == expected_result


def test_wrong_length_input(generate_random_account_card_name: Callable[[Optional[str], Optional[int]], str]) -> None:
    """Тестирует функцию с номером неправильной длины."""
    wrong_lengths: List[str] = [
        generate_random_account_card_name("Карта", 15),  # Слишком короткий номер карты
        generate_random_account_card_name("Карта", 17), # Слишком длинный номер карты
        generate_random_account_card_name("Счет", 19),  # Слишком короткий номер счета
        generate_random_account_card_name("Счет", 21)  # Слишком длинный номер счета
    ]

    for wrong_length in wrong_lengths:
        with pytest.raises(ValueError):
            widget.mask_account_card(wrong_length)


def test_invalid_type_for_account_card_name(generate_random_account_card_name: Callable[[Optional[str], Optional[int]], str]) -> None:
    """Тестирует функцию с неверным типом входного аргумента."""
    account_card_name = generate_random_account_card_name(None, None)
    match = re.search(r'\d+', account_card_name)
    if match:
        invalid_types: List[Any] = [
            int(match.group()),
            float(match.group()),
            None,
            {},
            [],
            ()
        ]
    else:
        invalid_types = [None, {}, [], ()]

    for invalid_type in invalid_types:
        with pytest.raises(Exception):
            widget.mask_account_card(invalid_type)

def test_get_date_valid() -> None:
    """Тестирует функцию с корректными значениями дат."""
    valid_date_list: list[str] = [
        "2018-06-30T02:08:58.425572",
        "2019-07-03T18:35:29.512364",
        "2018-09-12T21:27:25.241689",
        "2018-10-14T08:21:33.419441"
    ]
    for valid_date in valid_date_list:
        expected_date: str = datetime.datetime.strptime(valid_date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        assert widget.get_date(valid_date) == expected_date

def test_get_date_arg(generate_random_date: str) -> None:
    """Тестирует функцию с неверным типом аргумента."""
    match = re.search(r'\d+', generate_random_date)
    if match:
        invalid_types: List[Any] = [
            int(match.group()),
            float(match.group()),
            None,
            {},
            [],
            ()
        ]
    else:
        # Если совпадение не найдено, используем другие значения
        invalid_types = [None, {}, [], ()]

    for invalid_type in invalid_types:
        with pytest.raises(ValueError):
            widget.get_date(invalid_type)