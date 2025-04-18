import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)  # Создаю папку logs, если её нет

# Настройка обработчика для записи в файл
handler = logging.FileHandler("logs/masks.log", mode="w")
handler.setLevel(logging.DEBUG)

# Формат записи логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


def get_mask_card_number(card_number: str) -> str:
    """Принимает на вход номер карты и возвращает ее маску. Функция проверяет корректность входного аргумента."""
    try:
        logger.info(f"Начало обработки номера карты: {card_number}")
        if not isinstance(card_number, str):
            logger.error("TypeError: Входной аргумент должен быть строкой")
            raise TypeError("Входной аргумент должен быть строкой")
        if len(card_number) != 16:
            logger.error(
                f"ValueError: Длина номера карты должна быть 16 символов, но передана строка длиной {len(card_number)}"
            )
            raise ValueError(
                f"Длина номера карты должна быть 16 символов, но передана строка длиной {len(card_number)}"
            )
        if not card_number.isdigit():
            logger.error(f"ValueError: Номер карты должен содержать только цифры, но переданы символы: {card_number}")
            raise ValueError(f"Номер карты должен содержать только цифры, но переданы символы: {card_number}")
        mask_card_number = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        logger.info(f"Успешно сгенерирована маска номера карты: {mask_card_number}")
        return mask_card_number
    except Exception as e:
        logger.error(f"Ошибка при обработке номера карты: {e}", exc_info=True)
        raise


def get_mask_account(account_id: str) -> str:
    """Принимает на вход номер счета и возвращает его маску"""
    try:
        logger.info(f"Начало обработки номера счета: {account_id}")
        if not isinstance(account_id, str):
            logger.error("TypeError: Входной аргумент должен быть строкой")
            raise TypeError("Входной аргумент должен быть строкой")
        if len(account_id) != 20:
            logger.error(
                f"ValueError: Длина номера счёта должна быть 20 символов, но передана строка длиной {len(account_id)}"
            )
            raise ValueError(
                f"Длина номера счёта должна быть 20 символов, но передана строка длиной {len(account_id)}"
            )
        if not account_id.isdigit():
            logger.error(f"ValueError: Номер счёта должен содержать только цифры, но переданы символы: {account_id}")
            raise ValueError(f"Номер счёта должен содержать только цифры, но переданы символы: {account_id}")
        mask_account = "**" + account_id[-4:]
        logger.info(f"Успешно сгенерирована маска номера счета: {mask_account}")
        return mask_account
    except Exception as e:
        logger.error(f"Ошибка при обработке номера счета: {e}", exc_info=True)
        raise
