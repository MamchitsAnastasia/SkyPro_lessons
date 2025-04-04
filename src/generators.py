from typing import List, Dict, Iterator

def filter_by_currency (transactions: List[Dict[str, str]], code: str) -> Iterator[Dict[str, str]]:
    """Генератор принимает на вход список словарей, представляющих транзакции и возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной. """
    for transaction in transactions:
        if  transaction.get("code") == code:
            yield transaction

def transaction_descriptions (transactions: List[Dict[str, str]]) -> Iterator[str]:
    """Генератор принимает список словарей с транзакциями и возвращает описание каждой операции по очереди. """
    for transaction in transactions:
        yield transaction.get("description")

def card_number_generator (start: int, end: int) -> Iterator[str]:
    """Генератор принимает диапазон (начальное и конечное значения) и генерирует номер карты в этом диапазоне в формате XXXX XXXX XXXX XXXX. """
    for number in range(start, end + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[8:12] + " " + f"{number:016d}"[12:]

