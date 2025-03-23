def filter_by_state (list_of_operations, state="EXECUTED"):
    """Функция принимает список всех операций и возвращает список операций с указанным значением 'state', по умолчанию state = 'EXECUTED' """
    filtered_list_of_operations = []
    for operation in list_of_operations:
        if operation["state"] == state:
            filtered_list_of_operations.append(operation)

    return filtered_list_of_operations