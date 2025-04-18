import json
from unittest.mock import mock_open, patch

from src import utils


def test_load_valid_transactions() -> None:
    """Тестирует функцию load_transactions с корректным JSON-файлом"""
    test_data = [
        {"id": 441945886, "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}},
        {"id": 41428829, "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}},
    ]
    json_data = json.dumps(test_data)
    file_content = json_data
    mock_file = mock_open(read_data=file_content)
    mock_file.return_value.read.side_effect = [file_content[0], file_content]

    with patch("builtins.open", mock_file):
        result = utils.load_transactions("dummy_path.json")

        assert result == test_data
        mock_file.assert_called_once_with("dummy_path.json", "r", encoding="utf-8")


def test_file_not_found() -> None:
    """Тестирует функцию load_transactions в отсутствии файла"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = utils.load_transactions("nonexistent.json")
        assert result == []


def test_empty_file() -> None:
    """Тестирует функцию load_transactions если файл пуст"""
    mocked_open = mock_open(read_data="")
    with patch("builtins.open", mocked_open):
        result = utils.load_transactions("empty.json")
        assert result == []
        mocked_open.assert_called()


def test_invalid_json() -> None:
    """Тестирует функцию load_transactions  с некорректным JSON-файлом"""
    mocked_open = mock_open(read_data="{invalid json}")
    with patch("builtins.open", mocked_open):
        result = utils.load_transactions("bad.json")
        assert result == []
        mocked_open.assert_called()


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
    with patch("builtins.open", side_effect=PermissionError):
        result = utils.load_transactions("restricted.json")
        assert result == []


def test_file_with_whitespace_only() -> None:
    """Тестирует функцию load_transactions если в JSON-файле только пробелы"""
    mocked_open = mock_open(read_data="   \n\t   ")
    with patch("builtins.open", mocked_open):
        result = utils.load_transactions("whitespace.json")
        assert result == []
        mocked_open.assert_called()
