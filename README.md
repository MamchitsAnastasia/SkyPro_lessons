# Виджет банковских операций клиента

## Описание: 
Это учебный проект, представляющий модель виджета банковских операций клиента, написанный на Phyton.

Цель проекта: обучение работе с проектами в Pycharm и GitHub.

Статус разработки: в разработке.

Coverage report: [97%](http://localhost:63342/pythonproject/htmlcov/index.html?_ijt=315tro3c2643rg1p1lntajr0na&_ij_reload=RELOAD_ON_SAVE)

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
from src import processing
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
## ToDo:
Необходимо собрать функции в файл main.py

## Лицензия:
Этот проект лицензирован по [лицензии MIT](LICENSE).

Автор проекта: [Мамчиц Анастасия](https://github.com/MamchitsAnastasia)