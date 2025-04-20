import json
import pandas as pd
from unittest.mock import mock_open, patch, MagicMock
import pytest
from src import utils_CSV_Excel


def test_load_valid_csv_transactions() -> None:
    """Тестирует функцию load_transactions с корректным CSV-файлом"""
    test_data = [
        {"id": 441945886, "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}},
        {"id": 41428829, "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}},
    ]

    with patch("os.path.exists", return_value=True), \
            patch("os.path.getsize", return_value=100), \
            patch("pandas.read_csv", return_value=pd.DataFrame(test_data)):
        result = utils_CSV_Excel.load_transactions("dummy_path.csv")

        assert result == test_data


def test_load_valid_xlsx_transactions() -> None:
    """Тестирует функцию load_transactions с корректным XLSX-файлом"""
    test_data = [
        {"id": 441945886, "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}},
        {"id": 41428829, "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}},
    ]

    with patch("os.path.exists", return_value=True), \
            patch("os.path.getsize", return_value=100), \
            patch("pandas.read_excel", return_value=pd.DataFrame(test_data)):
        result = utils_CSV_Excel.load_transactions("dummy_path.xlsx")

        assert result == test_data

def test_file_not_found() -> None:
    """Тестирует функцию load_transactions в отсутствии файла"""
    with patch("os.path.exists", return_value=False):
        result = utils_CSV_Excel.load_transactions("nonexistent.csv")
        assert result == []


def test_empty_file() -> None:
    """Тестирует функцию load_transactions если файл пуст"""
    mocked_open = mock_open(read_data="")
    with patch("os.path.exists", return_value=True), \
            patch("os.path.getsize", return_value=0), \
            patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError):
        result = utils_CSV_Excel.load_transactions("empty.csv")
        assert result == []


def test_invalid_file_format() -> None:
    """Тестирует функцию load_transactions  с некорректным форматом"""
    with patch("os.path.exists", return_value=True):
        result = utils_CSV_Excel.load_transactions("unsupported.txt")
        assert result == []


def test_permission_error() -> None:
    """Тестирует функцию load_transactions если нет доступа к файлу"""
    with patch("pandas.read_csv", side_effect=PermissionError("No access")):
        result = utils_CSV_Excel.load_transactions("restricted.csv")
        assert result == []

def test_file_reading_error() -> None:
    """Тестирует функцию load_transactions при ошибке чтения файла"""
    with patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError("No data")):
        result = utils_CSV_Excel.load_transactions("corrupted.csv")
        assert result == []

