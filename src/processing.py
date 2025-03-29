from datetime import datetime

def filter_by_state(list_of_operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список всех операций и возвращает список операций с указанным значением 'state',
    по умолчанию 'state' = 'EXECUTED'"""
    filtered_list_of_operations: list[dict] = []
    for operation in list_of_operations:
        if operation["state"] == state:
            filtered_list_of_operations.append(operation)

    return filtered_list_of_operations


def sort_by_date(list_of_operations: list[dict], ascending: bool = False) -> list[dict]:
    """Функция принимает список операций и возвращает отсортированный по дате список операций в нужном порядке:
    True для сортировки по возрастанию, False для сортировки по убыванию, по умолчанию"""
    valid_operations = []
    for op in list_of_operations:
        if "date" in op:
            try:
                parsed_date = datetime.fromisoformat(op["date"])
                valid_operations.append({**op, "parsed_date": parsed_date})
            except ValueError:
                pass
    sorted_list_of_operations = sorted(
        valid_operations, key=lambda operation: operation["date"], reverse=not ascending
    )

    return [{k: v for k, v in op.items() if k != "parsed_date"} for op in sorted_list_of_operations]
