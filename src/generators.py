from typing import List, Dict, Iterator

def filter_by_currency (transactions: list[dict], code: str) -> Iterator[Dict[str, str]]:
    """Генератор принимает на вход список словарей, представляющих транзакции и возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной. """
    if not isinstance(transactions, list):
        raise TypeError("Переданное значение 'transactions' должно быть списком")
    if not isinstance(code, str):
        raise TypeError("Переданное значение 'code' должно быть строкой")
    if not transactions:
        raise ValueError("Список транзакций пуст.")
    for transaction in transactions:
        if not isinstance(transaction, dict):
            raise TypeError("Каждая транзакция в списке должна быть словарём")
        if "code" not in transaction:
            continue
        if  transaction.get("code") == code:
            yield transaction

def transaction_descriptions (transactions: list[dict]) -> Iterator[str]:
    """Генератор принимает список словарей с транзакциями и возвращает описание каждой операции по очереди. """
    if not isinstance(transactions, list):
        raise TypeError("Переданное значение 'transactions' должно быть списком")
    if not transactions:
        raise ValueError("Список транзакций пуст.")
    for transaction in transactions:
        if not isinstance(transaction, dict):
            raise TypeError("Каждая транзакция в списке должна быть словарём")
        if not isinstance(transaction.get("description"), str):
            raise TypeError("Значение по ключу 'description' должно быть строкой")
        if "description" not in  transaction:
            continue
        yield transaction.get("description")

def card_number_generator (start: int, end: int) -> Iterator[str]:
    """Генератор принимает диапазон (начальное и конечное значения) и генерирует номер карты в этом диапазоне в формате XXXX XXXX XXXX XXXX. """
    if not (start < end) and not (0 <= end < 9999999999999999):
        raise ValueError("Указан некорректный интервал для генерации.")
    for number in range(start, end + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[8:12] + " " + f"{number:016d}"[12:]



