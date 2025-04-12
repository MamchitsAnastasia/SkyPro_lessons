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
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == code:
                yield transaction
        except AttributeError:
            continue

def transaction_descriptions (transactions: list[dict]) -> Iterator[str]:
    """Генератор принимает список словарей с транзакциями и возвращает описание каждой операции по очереди. """
    if not isinstance(transactions, list):
        raise TypeError("Переданное значение 'transactions' должно быть списком")
    if not transactions:
        raise ValueError("Список транзакций пуст.")
    for transaction in transactions:
        if not isinstance(transaction, dict):
            raise TypeError("Каждая транзакция в списке должна быть словарём")
        description = transaction.get("description")
        if description is not None and isinstance(description, str):
            yield description

def card_number_generator (start: int, end: int) -> Iterator[str]:
    """Генератор принимает диапазон (начальное и конечное значения) и генерирует номер карты в этом диапазоне в формате XXXX XXXX XXXX XXXX. """
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Аргументы должны быть целыми числами")
    if start < 0 or end > 9999999999999999:
        raise ValueError("Числа должны быть в диапазоне от 0 до 9999999999999999")
    if start > end:
        raise ValueError("Начальное значение должно быть меньше или равно конечному")

    for number in range(start, end + 1):
        card_num = f"{number:016d}"
        yield f"{card_num[:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:]}"

