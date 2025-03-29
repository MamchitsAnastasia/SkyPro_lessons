import pytest
import re
import datetime
from src import widget
from src import processing

def test_valid_input():
    """Тестирует функцию с корректными номерами."""
    @pytest.mark.parametrize("account_card, expected_result",
        [
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ],
    )
    def test_valid_account_card_name(account_card, expected_result):
        result = widget.mask_account_card(account_card)
        assert result == expected_result


def test_wrong_length_input(generate_random_account_card_name):
    """Тестирует функцию с номером неправильной длины."""
    wrong_lengths = [
        generate_random_account_card_name("Карта", length=15),  # Слишком короткий номер карты
        generate_random_account_card_name("Карта", length=17), # Слишком длинный номер карты
        generate_random_account_card_name("Счет", length=19),  # Слишком короткий номер счета
        generate_random_account_card_name("Счет", length=21)  # Слишком длинный номер счета
    ]

    for wrong_length in wrong_lengths:
        with pytest.raises(ValueError):
            widget.mask_account_card(wrong_length)


def test_invalid_type_for_account_card_name(generate_random_account_card_name):
    """Тестирует функцию с неверным типом входного аргумента."""
    invalid_types = [
        int(re.search(r'\d+', generate_random_account_card_name()).group()),
        float(re.search(r'\d+', generate_random_account_card_name()).group()),
        None,
        {},
        [],
        ()
    ]

    for invalid_type in invalid_types:
        with pytest.raises(Exception):
            widget.mask_account_card(invalid_type)

def test_get_date_valid():
    """Тестирует функцию с корректными значениями дат."""
    valid_date_list = [
        "2018-06-30T02:08:58.425572",
        "2019-07-03T18:35:29.512364",
        "2018-09-12T21:27:25.241689",
        "2018-10-14T08:21:33.419441"
    ]
    for valid_date in valid_date_list:
        expected_date = datetime.datetime.strptime(valid_date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        assert widget.get_date(valid_date) == expected_date

def test_get_date_arg(generate_random_date):
    """Тестирует функцию с неверным типом аргумента."""
    invalid_types = [
        int(re.search(r'\d+', generate_random_date).group()),
        float(re.search(r'\d+', generate_random_date).group()),
        None,
        {},
        [],
        ()
    ]

    for invalid_type in invalid_types:
        with pytest.raises(ValueError):
            widget.get_date(invalid_type)