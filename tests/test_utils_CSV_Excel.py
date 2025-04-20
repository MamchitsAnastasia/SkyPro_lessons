from unittest.mock import patch

import pandas as pd

from src import utils_CSV_Excel


def test_load_valid_csv_transactions() -> None:
    """Тестирует функцию load_transactions с корректным CSV-файлом"""
    test_data = pd.DataFrame(
        {
            "id": [441945886, 41428829],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2019-08-26", "2019-07-03"],
            "amount": ["31957.58", "8221.37"],
            "currency_name": ["руб.", "USD"],
            "currency_code": ["RUB", "USD"],
            "description": ["Перевод", "Платеж"],
            "to": ["Счет 123", "Счет 456"],
        }
    )

    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=100),
        patch("pandas.read_csv", return_value=test_data),
    ):
        result = utils_CSV_Excel.load_transactions("dummy_path.csv")

        assert len(result) == 2
        assert result[0]["operationAmount"]["currency"]["name"] == "руб."
        assert result[1]["id"] == 41428829


def test_load_valid_xlsx_transactions() -> None:
    """Тестирует функцию load_transactions с корректным XLSX-файлом"""
    test_data = pd.DataFrame(
        {
            "id": [441945886, 41428829],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2019-08-26", "2019-07-03"],
            "amount": ["31957.58", "8221.37"],
            "currency_name": ["руб.", "USD"],
            "currency_code": ["RUB", "USD"],
            "description": ["Перевод", "Платеж"],
            "to": ["Счет 123", "Счет 456"],
            "from": ["Карта 123", None],  # Поле может быть None
        }
    )

    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=100),
        patch("pandas.read_excel", return_value=test_data),
    ):
        result = utils_CSV_Excel.load_transactions("dummy_path.xlsx")

        assert len(result) == 2
        assert result[0]["operationAmount"]["amount"] == "31957.58"
        assert result[1]["operationAmount"]["currency"]["code"] == "USD"


def test_file_not_found() -> None:
    """Тестирует функцию load_transactions в отсутствии файла"""
    with patch("os.path.exists", return_value=False):
        result = utils_CSV_Excel.load_transactions("nonexistent.csv")
        assert result == []


def test_empty_file() -> None:
    """Тестирует функцию load_transactions если файл пуст"""
    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=0),
        patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError),
    ):
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
