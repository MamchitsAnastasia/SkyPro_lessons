def get_mask_card_number(card_number: str) -> str:
    """Принимает на вход номер карты и возвращает ее маску. Функция проверяет корректность входного аргумента."""
    if not isinstance(card_number, str):
        raise TypeError("Входной аргумент должен быть строкой")
    if len(card_number) != 16:
        raise ValueError(f"Длина номера карты должна быть 16 символов, но передана строка длиной {len(card_number)}")
    if not card_number.isdigit():
        raise ValueError(f"Номер карты должен содержать только цифры, но переданы символы: {card_number}")
    mask_card_number = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
    return mask_card_number


def get_mask_account(account_id: str) -> str:
    """Принимает на вход номер счета и возвращает его маску"""
    if not isinstance(account_id, str):
        raise TypeError("Входной аргумент должен быть строкой")
    if len(account_id) != 20:
        raise ValueError(f"Длина номера счёта должна быть 20 символов, но передана строка длиной {len(account_id)}")
    if not account_id.isdigit():
        raise ValueError(f"Номер счёта должен содержать только цифры, но переданы символы: {account_id}")
    mask_account = "**" + account_id[-4:]
    return mask_account
