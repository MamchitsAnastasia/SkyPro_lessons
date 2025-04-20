import json
from unittest.mock import patch

import pandas as pd

from src import utils_JSON


def test_load_valid_json_transactions() -> None:
    """Тестирует функцию load_transactions с корректным JSON-файлом"""
    test_data = [
        {"id": 441945886, "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}},
        {"id": 41428829, "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}},
    ]

    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=100),
        patch("pandas.read_json", return_value=pd.DataFrame(test_data)),
    ):
        result = utils_JSON.load_transactions("dummy_path.json")

        assert result == test_data


def test_invalid_json_data() -> None:
    """Тестирует функцию load_transactions с некорректными JSON-данными"""
    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=100),
        patch("pandas.read_json", side_effect=json.JSONDecodeError("Invalid JSON", "dummy", 0)),
    ):
        result = utils_JSON.load_transactions("invalid.json")
        assert result == []


def test_file_not_found() -> None:
    """Тестирует функцию load_transactions в отсутствии файла"""
    with patch("os.path.exists", return_value=False):
        result = utils_JSON.load_transactions("nonexistent.json")
        assert result == []


def test_empty_file() -> None:
    """Тестирует функцию load_transactions если файл пуст"""
    with (
        patch("os.path.getsize", return_value=0),
        patch("pandas.read_json", side_effect=pd.errors.EmptyDataError("No data")),
    ):
        result = utils_JSON.load_transactions("empty.json")
        assert result == []


def test_unsupported_file_extension() -> None:
    """Тестирует функцию load_transactions с неподдерживаемым расширением файла"""
    with patch("os.path.exists", return_value=True):
        result = utils_JSON.load_transactions("unsupported.csv")
        assert result == []


def test_permission_error() -> None:
    """Тестирует функцию load_transactions если нет доступа к файлу"""
    with patch("pandas.read_json", side_effect=PermissionError("No access")):
        result = utils_JSON.load_transactions("restricted.json")
        assert result == []


def test_file_reading_error() -> None:
    """Тестирует функцию load_transactions при ошибке чтения файла"""
    with patch("pandas.read_json", side_effect=pd.errors.EmptyDataError("No data")):
        result = utils_JSON.load_transactions("corrupted.json")
        assert result == []
