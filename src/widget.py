import datetime
import re

from src import masks


def mask_account_card(account_card: str) -> str:
    """Принимает на вход наименование карты или счёта (тип и номер) и возвращает маску"""
    if not isinstance(account_card, str):
        raise ValueError("Входные данные должны быть строкой")

    account_card_num = re.findall(r"\d+", account_card)
    if not account_card_num:
        raise ValueError("Не найден номер карты/счёта в строке")

    if account_card.startswith("Счет"):
        if len(account_card_num[0]) != 20:
            raise ValueError("Номер счёта должен содержать 20 цифр")
        try:
            mask_account_card_num = masks.get_mask_account(account_card_num[0])
            return f"Счет {mask_account_card_num}"
        except Exception as e:
            raise ValueError(f"Ошибка маскирования счёта: {e}")
    else:
        if len(account_card_num[0]) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")
        try:
            mask_account_card_num = masks.get_mask_card_number(account_card_num[0])
            card_name = account_card[:-16].strip()
            return f"{card_name} {mask_account_card_num}"
        except Exception as e:
            raise ValueError(f"Ошибка маскирования карты: {e}")


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
