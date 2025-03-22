from src import masks


def mask_account_card(account_card: str) -> str:
    """Принимает на вход наименование карты или счёта (тип и номер) и возвращает маску"""

    if account_card[:4] == "Счет":
        mask_account_card_num = masks.get_mask_account(account_card[-20:])
        mask_account_card_all = account_card[:-20] + mask_account_card_num
    else:
        mask_account_card_num = masks.get_mask_card_number(account_card[-16:])
        mask_account_card_all = account_card[:-16] + mask_account_card_num

    return mask_account_card_all


def get_date(unformatted_date: str) -> str:
    """Принимает строку с датой и возвращает в формате ДД.ММ.ГГГГ"""
    formatted_date = unformatted_date[8:10] + "." + unformatted_date[5:7] + "." + unformatted_date[:4]
    return formatted_date
