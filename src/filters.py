import re
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
    transactions - список транзакций, categories - писок категорий для подсчета;
    и возвращает словарь с количеством транзакций по категориям"""
    category_counts = {category: 0 for category in categories}

    for transaction in transactions:
        description = transaction.get("description")
        if description is None or description == "":
            continue
        description = description.lower()
        for category in categories:
            if category is None:
                continue
            if description == category.lower():
                category_counts[category] += 1

    return category_counts
