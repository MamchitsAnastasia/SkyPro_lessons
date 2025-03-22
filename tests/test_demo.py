from src import widget


account_card = input("Введите номер карты или счёта: ")
print("Номер карты с маской: ", widget.mask_account_card(account_card))

unformatted_date = input("Введите дату: ")
print("Отформатированная дата: ", widget.get_date(unformatted_date))
