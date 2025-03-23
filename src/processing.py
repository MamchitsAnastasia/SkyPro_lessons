def filter_by_state (list_of_operations, state="EXECUTED"):
    """Функция принимает список всех операций и возвращает список операций с указанным значением 'state', по умолчанию state = 'EXECUTED' """
    filtered_list_of_operations = []
    for operation in list_of_operations:
        if operation["state"] == state:
            filtered_list_of_operations.append(operation)

    return filtered_list_of_operations

def sort_by_date (list_of_operations):
    """Функция принимает список операций и возвращает отсортированный по дате список операций"""
    sorted_list_of_operations = sorted(list_of_operations, key=lambda operation: operation["date"], reverse=True)

    return sorted_list_of_operations
