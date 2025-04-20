import json
import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)  # Создаю папку logs, если её нет

# Настройка обработчика для записи в файл
handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
handler.setLevel(logging.DEBUG)

# Формат записи логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


def load_transactions(file_path: str) -> list[dict]:
    """Функция загружает транзакции из JSON, путь к которому передается как аргумент"""
    try:
        logger.info(f"Попытка загрузить данные из файла: {file_path}")
        # Проверяю, существует ли файл
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден: {file_path}")
            return []

        # Проверяю, не пустой ли файл
        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл {file_path} пуст")
            return []

        # Определяю расширение файла
        file_ext = os.path.splitext(file_path)[1].lower()
        # Получаю расширение загруженного файла и привожу к нижнему регистру

        # Проверяю формат файла и читаю его
        if file_ext != ".json":
            logger.error(f"Неподдерживаемый формат файла: {file_ext}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Обработка вложенной структуры JSON
        if isinstance(data, dict) and "transactions" in data:
            transactions = data["transactions"]
        elif isinstance(data, list):
            transactions = data
        else:
            logger.error("Неподдерживаемая структура JSON")
            return []

        # Проверка обязательных полей
        required_fields = {"id", "state", "date", "operationAmount"}
        valid_transactions = []
        for transaction in transactions:
            if not all(field in transaction for field in required_fields):
                logger.warning(f"Пропущена транзакция с отсутствующими полями: {transaction.get('id')}")
                continue
            valid_transactions.append(transaction)

        logger.info(f"Успешно загружено {len(valid_transactions)} транзакций")
        return valid_transactions

    except Exception as e:  # Теперь перехватывает все исключения
        logger.error(f"Ошибка при загрузке данных из файла {file_path}: {e}", exc_info=True)
        return []
