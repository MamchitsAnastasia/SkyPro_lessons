from datetime import datetime


def filter_by_state(list_of_operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список всех операций и возвращает список операций с указанным значением 'state',
    по умолчанию 'state' = 'EXECUTED'"""
    if not list_of_operations:
        return []

    filtered_list_of_operations: list[dict] = []
    for operation in list_of_operations:
        if operation.get("state") == state:
            filtered_list_of_operations.append(operation)
    return filtered_list_of_operations


def sort_by_date(list_of_operations: list[dict], ascending: bool = False) -> list[dict]:
    """Функция принимает список операций и возвращает отсортированный по дате список операций в нужном порядке:
    True для сортировки по возрастанию, False для сортировки по убыванию, по умолчанию"""
    if not list_of_operations:
        return []

    dated_operations = []
    for op in list_of_operations:
        date_str = op.get("date")
        if not date_str:
            continue

        try:
            parsed_date = datetime.fromisoformat(date_str)
            dated_operations.append((parsed_date, op))
        except ValueError:
            continue

    sorted_list_of_operations = sorted(dated_operations, key=lambda item: item[0], reverse=not ascending)

    return [operation for (date, operation) in sorted_list_of_operations]
