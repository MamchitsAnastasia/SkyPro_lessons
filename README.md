# Виджет банковских операций клиента

## Описание: 
Это учебный проект, представляющий модель виджета банковских операций клиента, написанный на Phyton.

Цель проекта: обучение работе с проектами в Pycharm и GitHub.

Статус разработки: в разработке.

Coverage report: 96%  
Текущие метрики (актуально на 20.04.2025):

| Файл                     | Statements | Missing | Excluded | Coverage |
|--------------------------|------------|---------|----------|----------|
| `src/__init__.py`        | 0          | 0       | 0        | 100%     |
| `src/decorators.py`      | 29         | 0       | 0        | 100%     |
| `src/external_api.py`    | 20         | 0       | 0        | 100%     |
| `src/generators.py`      | 37         | 4       | 0        | 89%      |
| `src/masks.py`           | 46         | 0       | 0        | 100%     |
| `src/processing.py`      | 18         | 0       | 0        | 100%     |
| `src/utils_CSV_Excel.py` | 33         | 2       | 0        | 94%      |
| `src/utils_JSON.py`      | 31         | 4       | 0        | 87%      |
| `src/widget.py`          | 25         | 2       | 0        | 92%      |
| **Total**                | **239**    | **12**  | **0**    | **95%**  |

## Установка:

### 1. Клонируйте репозиторий:

```
git clone https://github.com/MamchitsAnastasia/SkyPro_lessons.git
```

### 2. Установите зависимости:

```
pip install -r requirements.txt
```

### 3. Импортируйте пакеты с функциями в модуль

```
from src import widget
from src import decorators
from src import external_api
from src import generators
from src import masks
from src import processing
from src import utils_CSV_Excel
from src import utils_JSON
```

## Использование:

На данный момент реализованы следующие функции: 

+ ### widget.mask_account_card(account_card)

Функция принимает на вход наименование карты или счёта (тип и номер) и возвращает маску 
в формате "Visa Platinum 7000 79** **** 6361"" или "Счет **4305" соответственно. Аргументом может быть строка типа  
**Visa Platinum 7000792289606361**,  
**Maestro 7000792289606361**,  
**Счет 73654108430135874305**
```
account_card = input("Введите номер карты или счёта: ")
print("Номер карты с маской: ", widget.mask_account_card(account_card))
```
**Результат выполнения функции:**   
Visa Platinum 7000 79** **** 6361,   
Maestro 7000 79** **** 6361,   
Счет **4305

+ ### widget.get_date(unformatted_date)

Функция принимает строку с датой в формате 
**2024-03-11T02:26:18.671407** и возвращает в формате **ДД.ММ.ГГГГ**
```
unformatted_date = "2024-03-11T02:26:18.671407"
print("Отформатированная дата: ", widget.get_date(unformatted_date))
```
**Результат выполнения функции:**  
11.03.2024

+ ### processing.filter_by_state(list_of_operations, state)

Функция принимает список всех операций и возвращает список операций с указанным значением 'state',  
по умолчанию 'state' = 'EXECUTED'
```
list_of_operations =[
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(processing.filter_by_state(list_of_operations, "CANCELED"))
```
**Результат выполнения функции:** 
```
[
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]
```
+ ### processing.sort_by_date(list_of_operations, ascending)

Функция принимает список операций и возвращает отсортированный по дате список операций в нужном порядке:  
True для сортировки по возрастанию, False для сортировки по убыванию (по умолчанию)
```
list_of_operations =[
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(processing.sort_by_date(list_of_operations, True))
```
**Результат выполнения функции:** 
```
[
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, 
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, 
{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
]
```

+ ### generators.filter_by_currency(transactions, code)

Функция принимает на вход список словарей, представляющих транзакции и 
возвращает итератор, который поочередно выдает транзакции, 
где валюта операции соответствует заданной (например, USD).
```
list_of_transactions = [
    {"id": 939719570, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 142264268,"operationAmount": {"currency": {"code": "EUR"}}}
]

print(list(generators.filter_by_currency(list_of_transactions, "USD")))
```
**Результат выполнения функции:** 
```
[
    {"id": 939719570, "operationAmount": {"currency": {"code": "USD"}}}
]
```
+ ### generators.transaction_descriptions(transactions)

Функция принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.
```
list_of_transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод с карты на карту"},
    {"description": "Пополнение счета"}
]

print(list(generators.transaction_descriptions(list_of_transactions)))
```
**Результат выполнения функции:** 
```
[
    "Перевод организации",
    "Перевод с карты на карту", 
    "Пополнение счета"
]
```

+ ### generators.card_number_generator(start, end)

Функция принимает начальное и конечное значения для генерации диапазона номеров и 
выдает номера банковских карт в формате XXXX XXXX XXXX XXXX , 
где X — цифра номера карты. Генератор может сгенерировать номера карт в заданном диапазоне 
от 0000 0000 0000 0001 до 9999 9999 9999 9999.
```
print(list(generators.card_number_generator(1, 3)))
```
**Результат выполнения функции:** 
```
[
    "0000 0000 0000 0001",
    "0000 0000 0000 0002",
    "0000 0000 0000 0003"
]
```


+ ### utils_CSV_Excel.load_transactions(file_path)

Функция загружает транзакции из CSV или XLSX-файлов, путь к которому передается как аргумент.  

```
transactions = utils_CSV_Excel.load_transactions("operations.csv")
print(f"Загружено {len(transactions)} транзакций")
```
**Результат выполнения функции:** 

```
Загружено 15 транзакций
```

+ ### utils_JSON.load_transactions(file_path)

Функция загружает транзакции из JSON-файла, путь к которому передается как аргумент.  

```
transactions = utils_JSON.load_transactions("operations.json")
print(f"Загружено {len(transactions)} транзакций")
```
**Результат выполнения функции:** 

```
Загружено 15 транзакций
```

+ ### external_api.convert_to_rub(transaction)

Функция переводит валюту транзакции в RUB, используя курсы валют с API exchangerates_data.  
Если валюта уже RUB - возвращает сумму без конвертации.  
При ошибках запроса к API возвращает 0.0.  
Требует API ключ в файле keys.env (переменная EXCHANGE_RATES_API_KEY).  

```
transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}
print(f"Сумма в рублях: {convert_to_rub(transaction)}")
```
**Результат выполнения функции:** 

```
Сумма в рублях: 7500.0 
```
(значение зависит от текущего курса USD)

+ ### log(filename)

Декоратор, который автоматически логирует начало и конец выполнения функции, 
а также ее результаты или возникшие ошибки.  
Декоратор принимает необязательный аргумент filename, который определяет, 
куда будут записываться логи (в файл или в консоль):

Если filename задан, логи записываются в указанный файл.  
Если filename не задан, логи выводятся в консоль.

```
@log()
def calculate(6, 2):
    return a / b
```
**Результат выполнения функции:** 
```
[
    calculate started.
    calculate ok. Result: 3
]
```

## ToDo:
Необходимо собрать функции в файл main.py

## Лицензия:
Этот проект лицензирован по [лицензии MIT](LICENSE).

Автор проекта: [Мамчиц Анастасия](https://github.com/MamchitsAnastasia)