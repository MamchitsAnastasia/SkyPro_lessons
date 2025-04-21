from src import decorators
from src import external_api
from src import filters
from src import generators
from src import masks
from src import processing
from src import utils_CSV_Excel
from src import utils_JSON
from src import widget

from datetime import datetime

VALID_STATES = ["EXECUTED", "CANCELED", "PENDING"]
POSITIVE_ANSWERS = ["ДА", "YES", "Y", "ХОЧУ", "КОНЕЧНО", "АГА", "УГУ", "OK", "OKAY", "ДАВАЙ", "ПОКАЖИ"]
NEGATIVE_ANSWERS = ["НЕТ", "NO", "N", "НЕ ХОЧУ", "НЕ НАДО", "НЕТ СПАСИБО", "НЕ ИНТЕРЕСУЕТ", "PAS", "NEIN", "NA"]

def main() -> None:
    """Основная функция программы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True: #Выбор файла
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        file_type = input()
        transactions = []

        if file_type == "1": #попытка обработать JSON-файл
            print(f"Для обработки выбран JSON-файл.\n")
            transactions = utils_JSON.load_transactions("data/operations.json")
            if not transactions:
                print("Не удалось загрузить транзакции или файл пуст. Попробуйте другой файл.\n")
                continue  # Возвращает к выбору формата
            else:
                break
        if file_type == "2":
            print(f"Для обработки выбран CSV-файл.\n")
            transactions = utils_CSV_Excel.load_transactions("data/transactions.csv")
            if not transactions:
                print("Не удалось загрузить транзакции или файл пуст. Попробуйте другой файл.\n")
                continue  # Возвращает к выбору формата
            else:
                break
        if file_type == "3":
            print(f"Для обработки выбран XLSX-файл.\n")
            transactions = utils_CSV_Excel.load_transactions("data/transactions_excel.xlsx")
            if not transactions:
                print("Не удалось загрузить транзакции или файл пуст. Попробуйте другой файл.\n")
                continue  # Возвращает к выбору формата
            else:
                break
        else:
            print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")
            continue #Повторяется, пока пользователь не выберет один из предложенных вариантов

    while True:  # Выбор статуса для фильтрации

        state = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).upper()

        if state in VALID_STATES: #Если статус доступен - фильтрую
            filtered_transactions = processing.filter_by_state(transactions, state)
            print(f'Операции отфильтрованы по статусу "{state}"')
            break
        else: #Если статус недоступен - запрашиваю заново
            print(f'Статус операции "{state}" недоступен.')
            continue

    while True:  # Фильтрация по дате
        sort_data_answer = input("Отсортировать операции по дате? Да/Нет\n").upper()
        if sort_data_answer in POSITIVE_ANSWERS:
            while True:
                order = input("Отсортировать по возрастанию или по убыванию?\n").lower()
                if "по возрастанию" in order:
                    filtered_transactions = processing.sort_by_date(filtered_transactions, True)

                    break
                elif "по убыванию" in order:
                    filtered_transactions = processing.sort_by_date(filtered_transactions, False)
                    break
                else:
                    print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")
                    continue
            break
        elif sort_data_answer in NEGATIVE_ANSWERS:
            break
        else:  # Если ответ некорректен - запрашиваю заново
            print("Пожалуйста, ответьте 'Да' или 'Нет'")
            continue

    while True:  # Фильтрация по валюте
        sort_rub_answer = input("Выводить только рублевые тразакции? Да/Нет\n").upper()
        if sort_rub_answer in POSITIVE_ANSWERS:
            filtered_transactions = list(generators.filter_by_currency(filtered_transactions, "RUB"))
            break
        elif sort_rub_answer in NEGATIVE_ANSWERS:
            break
        else:  # Если ответ некорректен - запрашиваю заново
            print("Пожалуйста, ответьте 'Да' или 'Нет'")
            continue


    while True:  # Фильтрация по описанию
        sort_description_answer = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").upper()
        if sort_description_answer in POSITIVE_ANSWERS:
            search_word = input("Введите слово для поиска в описании: ")
            filtered_transactions = filters.filter_transactions_by_description(filtered_transactions, search_word)
            break
        elif sort_description_answer in NEGATIVE_ANSWERS:
            break
        else:  # Если ответ некорректен - запрашиваю заново
            print("Пожалуйста, ответьте 'Да' или 'Нет'")
            continue



    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    else:
        print("Распечатываю итоговый список транзакций...")
        print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}\n")

        for transaction in filtered_transactions:
            # Инициализация всех переменных со значениями по умолчанию
            date = ""
            description = ""
            amount = "0"
            name_of_currency = ""
            from_account = None
            to_account = None
            masked_from = ""
            masked_to = ""

            try:
                raw_date  = transaction.get("date", "")
                formatted_date = ""
                if raw_date:
                    try:
                        if isinstance(raw_date, datetime):
                        # Если дата уже datetime
                            formatted_date = raw_date.strftime("%d.%m.%Y")
                        else:
                        # Если транзакции не были отсортированы и дата подаётся строкой
                            dt = datetime.fromisoformat(raw_date) # Сперва переводим в datetime
                            formatted_date = dt.strftime("%d.%m.%Y")
                    except (ValueError, TypeError):
                        formatted_date = raw_date

                description = transaction.get("description", "")

                operation_amount = transaction.get("operationAmount", {})
                amount = str(operation_amount.get("amount", "0")) if operation_amount else "0"
                currency = operation_amount.get("currency", {}) if operation_amount else {}
                name_of_currency = currency.get("name", "") if currency else ""

                from_account = transaction.get("from")
                to_account = transaction.get("to")

                if from_account:
                    masked_from = widget.mask_account_card(str(from_account))
                if to_account:
                    masked_to = widget.mask_account_card(str(to_account))

            except Exception as e:
                print(f"Ошибка обработки транзакции: {e}. Транзакция пропущена.\n")
                continue

            print(f"{formatted_date} {description}")

            if from_account and to_account:
                print(f"{masked_from} -> {masked_to}")
            elif from_account:
                print(f"{masked_from}")
            elif to_account:
                print(f"{masked_to}")

            print(f"Сумма: {amount} {name_of_currency}\n")

    return


if __name__ == "__main__":
    main()



