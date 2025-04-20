import pytest
from unittest.mock import patch
import sys
import os
from datetime import datetime

# Добавляю путь к проекту
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main


def test_main_flow_json_file(capsys):
    """Тестирует main с JSON файлом"""
    # Создаю корректные тестовые данные
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "1",  # выбор JSON
        "EXECUTED",  # статус транзакции
        "Нет",  # не сортировать по дате
        "Нет",  # не фильтровать по рублям
        "Нет"  # не фильтровать по описанию
    ]

    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    output = captured.out

    # Проверяю ключевые элементы вывода
    assert "Для обработки выбран JSON-файл" in output
    assert "EXECUTED" in output
    assert "9824.07 USD" in output
    assert "Счет **6952" in output
    assert "Счет **6702" in output

def test_main_sort_ascending(capsys):
    """Тестирует main с сортировкой по возрастанию даты"""
    sample_transactions = [
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "1",  # выбор JSON
        "EXECUTED",  # статус транзакции
        "Да",  # сортировать по дате
        "по возрастанию",  # сортировать по возрастанию
        "Нет",  # не фильтровать по рублям
        "Нет"  # не фильтровать по описанию
    ]

    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    output = captured.out
    # Проверяю наличие обеих дат в правильном порядке
    assert "30.06.2018" in output
    assert "04.04.2019" in output
    assert output.find("30.06.2018") < output.find("04.04.2019")

def test_main_sort_descending(capsys):
    """Тестирует main с сортировкой по убыванию даты"""
    # Выбираю транзакций со статусом EXECUTED
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "1",  # выбор JSON
        "EXECUTED",  # статус транзакции
        "Да",  # сортировать по дате
        "по убыванию", # сортировать по убыванию
        "Нет",  # не фильтровать по рублям
        "Нет"  # не фильтровать по описанию
    ]


    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    output = captured.out

    # Проверяю наличие обеих дат в правильном порядке
    assert "30.06.2018" in output
    assert "04.04.2019" in output
    assert output.find("04.04.2019") < output.find("30.06.2018")

def test_main_filter_rub(capsys):
    """Тестирует main с фильтрацией по рублям"""
    sample_transactions = [
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]

    # Мокаею функцию filter_by_currency, чтобы она действительно фильтровала по RUB
    def mock_filter_by_currency(transactions, currency):
        return [t for t in transactions
                if t["operationAmount"]["currency"]["code"] == currency]

    # Создаю корректные входные значения
    input_values = [
        "1",  # выбор JSON
        "EXECUTED",  # статус транзакции
        "Нет",  # не сортировать по дате
        "Да",  # фильтровать по рублям
        "Нет"  # не фильтровать по описанию
    ]

    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('main.generators.filter_by_currency', side_effect=mock_filter_by_currency):
            with patch('builtins.input', side_effect=input_values):
                main()

    captured = capsys.readouterr()
    output = captured.out

    # Проверяем, что RUB транзакция есть в выводе, а USD - нет
    assert "Перевод со счета на счет" in output
    assert "43318.34 руб." in output
    assert "Перевод организации" not in output
    assert "9824.07 USD" not in output


def test_main_filter_description(capsys):
    """Тестирует main с фильтрацией по описанию"""
    # Выбираю транзакций с статусом EXECUTED
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "1",  # выбор JSON
        "EXECUTED",  # статус транзакции
        "Нет",  # не сортировать по дате
        "Нет",  # не фильтровать по рублям
        "Да", # фильтровать по описанию
        "Перевод организации",  # описание
    ]

    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    output = captured.out

    assert "Перевод организации" in output
    assert "Перевод со счета на счет" not in output


def test_main_no_transactions(capsys):
    """Тестирует main без подходящих транзакций"""
    # Выбираю транзакций со статусом EXECUTED
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        }
    ]
    # Создаю корректные входные значения
    input_values = [
        "1",  # выбор JSON
        "PENDING",  # статус транзакции
        "Нет",  # не сортировать по дате
        "Нет",  # не фильтровать по рублям
        "Нет",  # не фильтровать по описанию
    ]

    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    output = captured.out

    assert "Не найдено ни одной транзакции" in output


def test_main_csv_file(capsys):
    """Тестирует main с CSV файлом"""
    sample_transactions = [
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "2",  # выбор CSV
        "EXECUTED",  # статус транзакции
        "Нет",  # не сортировать по дате
        "Нет",  # не фильтровать по рублям
        "Нет",  # не фильтровать по описанию
    ]

    with patch('main.utils_CSV_Excel.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    assert "Для обработки выбран CSV-файл" in captured.out
    assert "Перевод с карты на карту" in captured.out


def test_main_xlsx_file(capsys):
    """Тестирует main с XLSX файлом"""
    sample_transactions = [
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "3",  # выбор XLSX
        "EXECUTED",  # статус транзакции
        "Нет",  # не сортировать по дате
        "Нет",  # не фильтровать по рублям
        "Нет",  # не фильтровать по описанию
    ]

    with patch('main.utils_CSV_Excel.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    assert "Для обработки выбран XLSX-файл" in captured.out
    assert "Перевод со счета на счет" in captured.out


def test_main_invalid_file_choice(capsys):
    """Тестирует main при неверном выборе формата файла"""
    # Подготовка тестовых данных
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "4",  # первый неверный выбор файла
        "1",  # затем верный выбор (JSON)
        "EXECUTED",  # статус транзакции
        "Нет",  # не сортировать по дате
        "Нет",  # не фильтровать по рублям
        "Нет"  # не фильтровать по описанию
    ]

    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    output = captured.out

    assert "Неверный выбор. Пожалуйста, введите 1, 2 или 3" in output
    assert "Перевод организации" in output


def test_main_invalid_state(capsys):
    """Тестирует main при неверном статусе транзакции"""
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "1",  # выбор JSON файла
        "INVALID",  # первый неверный статус
        "EXECUTED",  # затем верный статус
        "Нет",  # не сортировать по дате
        "Нет",  # не фильтровать по рублям
        "Нет"  # не фильтровать по описанию
    ]

    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    output = captured.out

    assert 'Статус операции "INVALID" недоступен' in output
    assert "Перевод организации" in output


def test_main_date_error_handling(capsys):
    """Тестирует main при неформатируемой дате"""
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "invalid_date",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]

    # Создаю корректные входные значения
    input_values = [
        "1",  # выбор JSON файла
        "EXECUTED",  # затем верный статус
        "Нет",  # не сортировать по дате
        "Нет",  # не фильтровать по рублям
        "Нет"  # не фильтровать по описанию
    ]

    with patch('main.utils_JSON.load_transactions', return_value=sample_transactions):
        with patch('builtins.input', side_effect=input_values):
            main()

    captured = capsys.readouterr()
    output = captured.out
    assert "invalid_date" in output
    assert "Перевод организации" in output
