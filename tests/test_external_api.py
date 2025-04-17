from unittest.mock import Mock, patch

import pytest
import requests

from src import external_api


def test_rub_transaction():
    """Тестирует функцию convert_to_rub когда валюта уже в рублях"""
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    assert external_api.convert_to_rub(transaction) == 100.0


@patch("requests.get")
def test_usd_to_rub_conversion(mock_get):
    """Тестирует функцию convert_to_rub для успешной конвертации USD в RUB"""
    mock_response = Mock()  # Создаю фейковый объект, который имитирует реальный ответ от API.
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_response.raise_for_status.return_value = None  # Имитирую успешный ответ
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    assert external_api.convert_to_rub(transaction) == 905.0


@patch("requests.get")
def test_api_request_exception(mock_get):
    """Тестирует функцию convert_to_rub когда API возвращает ошибку"""
    mock_get.side_effect = requests.RequestException("API недоступен")  # Имитирую неуспешный ответ
    transaction = {"operationAmount": {"amount": "50", "currency": {"code": "EUR"}}}
    assert external_api.convert_to_rub(transaction) == 0.0


def test_missing_amount():
    """Тестирует функцию convert_to_rub когда в транзакции нет суммы"""
    transaction = {"operationAmount": {"currency": {"code": "USD"}}}
    assert external_api.convert_to_rub(transaction) == 0.0


def test_missing_currency():
    """Тестирует функцию convert_to_rub когда в транзакции нет валюты"""
    transaction = {"operationAmount": {"amount": "100"}}
    assert external_api.convert_to_rub(transaction) == 100.0  # Должен использовать RUB по умолчанию


def test_missing_operation_amount():
    """Тестирует функцию convert_to_rub когда нет operationAmount"""
    transaction = {}
    assert external_api.convert_to_rub(transaction) == 0.0


@patch("requests.get")
def test_api_timeout(mock_get):
    """Тестирует функцию convert_to_rub, проверяя время ожидания ответа"""
    mock_get.side_effect = requests.Timeout("Превышено время ожидания")
    transaction = {"operationAmount": {"amount": "75", "currency": {"code": "CNY"}}}
    assert external_api.convert_to_rub(transaction) == 0.0


def test_non_numeric_amount():
    """Тестирует функцию convert_to_rub на обработку нечисловой суммы"""
    transaction = {"operationAmount": {"amount": "abc", "currency": {"code": "USD"}}}
    assert external_api.convert_to_rub(transaction) == 0.0


def test_missing_currency_code():
    """Тестирует функцию convert_to_rub когда в currency нет code"""
    transaction = {"operationAmount": {"amount": "100", "currency": {}}}
    assert external_api.convert_to_rub(transaction) == 100.0  # Должен использовать RUB по умолчанию
