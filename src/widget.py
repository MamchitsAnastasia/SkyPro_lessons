import re
import datetime
from src import masks


def mask_account_card(account_card: str) -> str:
    """Принимает на вход наименование карты или счёта (тип и номер) и возвращает маску"""

    if account_card[:4] == "Счет":
        if re.findall(r'\d+', account_card) != 20:
            raise ValueError("Введён некорректный номер счёта")
        mask_account_card_num = masks.get_mask_account(account_card[-20:])
        mask_account_card_all = account_card[:-20] + mask_account_card_num
    else:
        if re.findall(r'\d+', account_card) != 16:
            raise ValueError("Введён некорректный номер карты")
        mask_account_card_num = masks.get_mask_card_number(account_card[-16:])
        mask_account_card_all = account_card[:-16] + mask_account_card_num

    try:
        return mask_account_card_all
    except Exception as e:
        print(f"Ошибка при создании маски: {e}")
        return ""


def get_date(unformatted_date: str) -> str:
    """Принимает строку с датой и возвращает в формате ДД.ММ.ГГГГ"""
    if not isinstance(unformatted_date, str):
        raise ValueError(f"Переданное значение должно быть строкой, а не {type(unformatted_date).__name__}")
    try:
        datetime.datetime.strptime(unformatted_date, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        raise ValueError("Неверный формат даты: {}".format(unformatted_date))
    formatted_date = unformatted_date[8:10] + "." + unformatted_date[5:7] + "." + unformatted_date[:4]
    return formatted_date
