import json
from unittest.mock import patch, mock_open
from pytest import raises

from src import utils_JSON


def test_load_valid_json_transactions() -> None:
    """Тестирует функцию load_transactions с корректным JSON-файлом"""
    test_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"}
            }
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "USD", "code": "USD"}
            }
        }
    ]

    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=100),
        patch("builtins.open", mock_open(read_data=json.dumps(test_data))),
        patch("json.load", return_value=test_data)
    ):
        result = utils_JSON.load_transactions("dummy_path.json")

        assert len(result) == 2
        assert result[0]["operationAmount"]["currency"]["name"] == "руб."
        assert result[1]["id"] == 41428829


def test_invalid_json_data() -> None:
    """Тестирует функцию load_transactions с некорректными JSON-данными"""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data="invalid json")),
        patch("json.load", side_effect=json.JSONDecodeError("Ошибка", "doc", 1))
    ):
        result = utils_JSON.load_transactions("invalid.json")
        assert result == []


def test_nested_json_structure() -> None:
    """Тестирует обработку JSON с вложенной структурой"""
    test_data = {
        "transactions": [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T00:00:00",
                "operationAmount": {
                    "amount": "100",
                    "currency": {"name": "руб.", "code": "RUB"}
                }
            }
        ]
    }

    json_str = json.dumps(test_data)

    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=100),
        patch("builtins.open", mock_open(read_data=json_str)),
        patch("json.load", return_value=test_data)
    ):
        result = utils_JSON.load_transactions("nested.json")
        assert len(result) == 1
        assert result[0]["id"] == 1

def test_missing_required_fields() -> None:
    """Тестирует отсеивание транзакций без обязательных полей"""
    test_data = [
        {"id": 1, "state": "EXECUTED"},  # Неполные данные
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2023-01-01T00:00:00",
            "operationAmount": {
                "amount": "100",
                "currency": {"name": "руб.", "code": "RUB"}
            }
        }
    ]

    json_str = json.dumps(test_data)

    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=100),
        patch("builtins.open", mock_open(read_data=json_str)),
        patch("json.load", return_value=test_data)
    ):
        result = utils_JSON.load_transactions("missing_fields.json")
        assert len(result) == 1
        assert result[0]["id"] == 2
