from src import widget
from src import processing

list_of_operations =[
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

account_card = input("Введите номер карты или счёта: ")
print("Номер карты с маской: ", widget.mask_account_card(account_card))

unformatted_date = input("Введите дату: ")
print("Отформатированная дата: ", widget.get_date(unformatted_date))

print("Тестовые изменения для инициализации новой ветки 'develop'")

print(processing.filter_by_state(list_of_operations, "CANCELED"))
print(processing.sort_by_date(list_of_operations, True))
