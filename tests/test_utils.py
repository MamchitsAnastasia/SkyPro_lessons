import json
import pandas as pd
from unittest.mock import mock_open, patch, MagicMock
import pytest
from src import utils


def test_load_valid_json_transactions() -> None:
    """Тестирует функцию load_transactions с корректным JSON-файлом"""
    test_data = [
        {"id": 441945886, "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}},
        {"id": 41428829, "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}},
    ]

    with patch("pandas.read_json", return_value=pd.DataFrame(test_data)) as mock_read:
        result = utils.load_transactions("dummy_path.json")

        assert result == test_data
        mock_file.assert_called_once_with("dummy_path.json", "r", encoding="utf-8")


def test_load_valid_csv_transactions() -> None:
    """Тестирует функцию load_transactions с корректным CSV-файлом"""
    test_data = [
        {"id": 441945886, "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}},
        {"id": 41428829, "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}},
    ]

    with patch("pandas.read_csv", return_value=pd.DataFrame(test_data)) as mock_read:
        result = utils.load_transactions("dummy_path.csv")

        assert result == test_data
        mock_read.assert_called_once_with("dummy_path.csv", encoding='utf-8')


def test_load_valid_xlsx_transactions() -> None:
    """Тестирует функцию load_transactions с корректным XLSX-файлом"""
    test_data = [
        {"id": 441945886, "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}},
        {"id": 41428829, "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}},
    ]

    with patch("pandas.read_excel", return_value=pd.DataFrame(test_data)) as mock_read:
        result = utils.load_transactions("dummy_path.xlsx")

        assert result == test_data
        mock_read.assert_called_once_with("dummy_path.xlsx")

def test_file_not_found() -> None:
    """Тестирует функцию load_transactions в отсутствии файла"""
    with patch("os.path.exists", return_value=False):
        result = utils.load_transactions("nonexistent.json")
        assert result == []


def test_empty_file() -> None:
    """Тестирует функцию load_transactions если файл пуст"""
    mocked_open = mock_open(read_data="")
    with patch("os.path.getsize", return_value=0):
        result = utils.load_transactions("empty.json")
        assert result == []


def test_invalid_file_format() -> None:
    """Тестирует функцию load_transactions  с некорректным форматом"""
    result = utils.load_transactions("unsupported.txt")
    assert result == []


def test_not_list_data() -> None:
    """Тестирует функцию load_transactions если JSON есть, но это не список"""
    test_data = {"transaction": {"id": 1, "amount": 100}}
    mocked_open = mock_open(read_data=json.dumps(test_data))
    with patch("builtins.open", mocked_open):
        result = utils.load_transactions("not_list.json")
        assert result == []
        mocked_open.assert_called()


def test_permission_error() -> None:
    """Тестирует функцию load_transactions если нет доступа к файлу"""
    with patch("pandas.read_json", side_effect=PermissionError("No access")):
        result = utils.load_transactions("restricted.json")
        assert result == []

def test_file_reading_error() -> None:
    """Тестирует функцию load_transactions при ошибке чтения файла"""
    with patch("pandas.read_json", side_effect=pd.errors.EmptyDataError("No data")) as mock_read:
        result = utils.load_transactions("corrupted.json")
        assert result == []
        mock_read.assert_called_once_with("corrupted.json")

def test_file_with_whitespace_only() -> None:
    """Тестирует функцию load_transactions если в JSON-файле только пробелы"""
    mocked_open = mock_open(read_data="   \n\t   ")
    with patch("builtins.open", mocked_open):
        result = utils.load_transactions("whitespace.json")
        assert result == []
        mocked_open.assert_called()
