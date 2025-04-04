from typing import Any, Callable, List

import pytest

from src import masks


def test_valid_card_numbers(generate_random_card_number: Callable[[], str]) -> None:
    """Тестирует функцию с корректными номерами карт."""
    valid_card_numbers: List[str] = [
        generate_random_card_number(),
        generate_random_card_number(),
        generate_random_card_number(),
    ]

    for card_number in valid_card_numbers:
        expected_output: str = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        assert masks.get_mask_card_number(card_number) == expected_output


def test_wrong_length_for_card_number(generate_random_card_number: Callable[[int], str]) -> None:
    """Тестирует функцию с номером карты неправильной длины."""
    wrong_lengths: List[str] = [
        generate_random_card_number(15),  # Слишком короткий
        generate_random_card_number(17),  # Слишком длинный
    ]

    for wrong_length in wrong_lengths:
        with pytest.raises(ValueError):
            masks.get_mask_card_number(wrong_length)


def test_non_digit_for_card_number(generate_random_card_number: Callable[[], str]) -> None:
    """Тестирует функцию с номером карты, содержащим нецифровые символы."""
    non_digits: List[str] = [
        generate_random_card_number().replace("0", "a"),  # Замена одной цифры на букву
        generate_random_card_number().replace("1", "!"),  # Замена другой цифры на спецсимвол
    ]

    for non_digit in non_digits:
        with pytest.raises(ValueError):
            masks.get_mask_card_number(non_digit)


def test_invalid_type_for_card_number(generate_random_card_number: Callable[[], str]) -> None:
    """Тестирует функцию с неверным типом входного аргумента."""
    invalid_types: List[Any] = [
        int(generate_random_card_number()),
        float(generate_random_card_number()),
        None,
        {},
        [],
        (),
    ]

    for invalid_type in invalid_types:
        with pytest.raises(TypeError):
            masks.get_mask_card_number(invalid_type)


def test_valid_account_id(generate_random_account_id: Callable[[], str]) -> None:
    """Тестирует функцию с корректными номерами счетов."""
    valid_account_id: List[str] = [
        generate_random_account_id(),
        generate_random_account_id(),
        generate_random_account_id(),
    ]

    for account_id in valid_account_id:
        expected_output = "**" + account_id[-4:]
        assert masks.get_mask_account(account_id) == expected_output


def test_wrong_length_account_number(generate_random_account_id: Callable[[int], str]) -> None:
    """Тестирует функцию с номером счетов неправильной длины."""
    wrong_lengths: List[str] = [
        generate_random_account_id(19),  # Слишком короткий
        generate_random_account_id(21),  # Слишком длинный
    ]

    for wrong_length in wrong_lengths:
        with pytest.raises(ValueError):
            masks.get_mask_account(wrong_length)


def test_non_digit_for_account_id(generate_random_account_id: Callable[[], str]) -> None:
    """Тестирует функцию с номером счета, содержащим нецифровые символы."""
    non_digits: List[str] = [
        generate_random_account_id().replace("0", "a"),  # Замена одной цифры на букву
        generate_random_account_id().replace("1", "!"),  # Замена другой цифры на спецсимвол
    ]

    for non_digit in non_digits:
        with pytest.raises(ValueError):
            masks.get_mask_account(non_digit)


def test_invalid_type_for_account_id(generate_random_account_id: Callable[[], str]) -> None:
    """Тестирует функцию с неверным типом входного аргумента."""
    invalid_types: List[Any] = [
        int(generate_random_account_id()),
        float(generate_random_account_id()),
        None,
        {},
        [],
        (),
    ]

    for invalid_type in invalid_types:
        with pytest.raises(TypeError):
            masks.get_mask_account(invalid_type)
