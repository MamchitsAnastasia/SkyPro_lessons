import json
import pytest
from unittest.mock import patch, mock_open
from src import utils


def test_load_valid_transactions():
    """Тестирует функцию load_transactions с корректным JSON-файлом"""
    test_data = [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 50, "currency": "USD"}
    ]
    mocked_open = mock_open(read_data=json.dumps(test_data))
    with patch('builtins.open', mocked_open):
        result = utils.load_transactions('dummy.json')
        assert result == test_data
        mocked_open.assert_called()


def test_file_not_found():
    """Тестирует функцию load_transactions в отсутствии файла"""
    with patch('builtins.open', side_effect=FileNotFoundError):
        result = utils.load_transactions('nonexistent.json')
        assert result == []


def test_empty_file():
    """Тестирует функцию load_transactions если файл пуст"""
    mocked_open = mock_open(read_data='')
    with patch('builtins.open', mocked_open):
        result = utils.load_transactions('empty.json')
        assert result == []
        mocked_open.assert_called()


def test_invalid_json():
    """Тестирует функцию load_transactions  с некорректным JSON-файлом"""
    mocked_open = mock_open(read_data='{invalid json}')
    with patch('builtins.open', mocked_open):
        result = utils.load_transactions('bad.json')
        assert result == []
        mocked_open.assert_called()


def test_not_list_data():
    """Тестирует функцию load_transactions если JSON есть, но это не список"""
    test_data = {"transaction": {"id": 1, "amount": 100}}
    mocked_open = mock_open(read_data=json.dumps(test_data))
    with patch('builtins.open', mocked_open):
        result = utils.load_transactions('not_list.json')
        assert result == []
        mocked_open.assert_called()


def test_permission_error():
    """Тестирует функцию load_transactions если нет доступа к файлу"""
    with patch('builtins.open', side_effect=PermissionError):
        result = utils.load_transactions('restricted.json')
        assert result == []


def test_file_with_whitespace_only():
    """Тестирует функцию load_transactions если в JSON-файле только пробелы"""
    mocked_open = mock_open(read_data='   \n\t   ')
    with patch('builtins.open', mocked_open):
        result = utils.load_transactions('whitespace.json')
        assert result == []
        mocked_open.assert_called()