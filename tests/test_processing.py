from typing import Any, Dict, List

import pytest

from src import processing

sample_operations_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


@pytest.fixture
def operations_data() -> List[Dict[str, Any]]:
    return sample_operations_data


def test_filter_by_state_default(operations_data: List[Dict[str, Any]]) -> None:
    """Тестирует функцию с корректными данными, статус по умолчанию 'EXECUTED'."""
    result = processing.filter_by_state(operations_data)
    expected_result: List[Dict[str, Any]] = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert result == expected_result


def test_filter_by_state_multiple_executed(operations_data: List[Dict[str, Any]]) -> None:
    """Тестирует функцию с корректными данными, статус 'CANCELED'."""
    result = processing.filter_by_state(operations_data, state="CANCELED")
    expected_result: List[Dict[str, Any]] = [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    assert result == expected_result


def test_filter_by_state_no_match() -> None:
    """Тестирует функцию при отсутствии статуса 'EXECUTED'."""
    operations_data_without_executed = [
        {"id": 41428829, "state": "PENDING", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "COMPLETED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    result = processing.filter_by_state(operations_data_without_executed)
    expected_result: List[Dict[str, Any]] = []
    assert result == expected_result


def test_sort_by_date_default(operations_data: List[Dict[str, Any]]) -> None:
    """Тестирует функцию с корректными данными, сортировка по умолчанию - по убыванию."""
    result = processing.sort_by_date(operations_data)
    expected_result: List[Dict[str, Any]] = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert result == expected_result


def test_sort_by_date_multiple_executed(operations_data: List[Dict[str, Any]]) -> None:
    """Тестирует функцию с корректными данными, сортировка по возрастанию'."""
    result = processing.sort_by_date(operations_data, True)
    expected_result: List[Dict[str, Any]] = [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]
    assert result == expected_result


def test_sort_by_date_no_match() -> None:
    """Тестирует функцию при отсутствии даты."""
    operations_data_without_executed = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "Invalid Date"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED"},
    ]
    result = processing.sort_by_date(operations_data_without_executed)
    expected_result: List[Dict[str, Any]] = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    ]
    assert result == expected_result
