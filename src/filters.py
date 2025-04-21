import re
from collections import Counter
from typing import Any


def filter_transactions_by_description(transactions: list[dict[str, Any]], search_string: str) -> list[dict[str, Any]]:
    """Функция фильтрует транзакции по наличию строки поиска в описании:
    transactions - список транзакций, search_string - строка для поиска в описании;
    и возвращает отфильтрованный список транзакций"""
    if not search_string:
        return []
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [
        transaction
        for transaction in transactions
        if transaction.get("description") and pattern.search(transaction["description"])
    ]


def count_transactions_by_category(transactions: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Функция подсчитывает количество транзакций по категориям:
    transactions - список транзакций, categories - список категорий для подсчета;
    и возвращает словарь с количеством транзакций по категориям"""

    categories_lower = [category.lower() for category in categories if category is not None]

    descriptions = [
        transaction["description"].lower()
        for transaction in transactions
        if transaction.get("description") and transaction["description"].lower() in categories_lower
    ]

    counter = Counter(descriptions)

    result = {}
    for category in categories:
        if category is not None:
            lower_category = category.lower()
            result[category] = counter.get(lower_category, 0)

    return result
