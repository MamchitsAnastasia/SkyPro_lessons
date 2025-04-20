import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)  # Создаю папку logs, если её нет

# Настройка обработчика для записи в файл
handler = logging.FileHandler("logs/utils.log", mode="w", encoding='utf-8')
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
        file_ext = os.path.splitext(file_path)[
            1
        ].lower()  # Получаю расширение загруженного файла и привожу к нижнему регистру

        # Проверяю формат файла и читаю его
        if file_ext == ".json":
            df = pd.read_json(file_path)
        else:
            logger.error(f"Неподдерживаемый формат файла: {file_ext}")
            return []

        # Конвертирую DataFrame в список словарей
        result = df.to_dict("records")
        logger.info(f"Успешно загружено {len(result)} транзакций из файла {file_path}")
        return result

    except Exception as e:  # Теперь перехватывает все исключения
        logger.error(f"Ошибка при загрузке данных из файла {file_path}: {e}", exc_info=True)
        return []
