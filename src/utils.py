import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)  # Создаю папку logs, если её нет

# Настройка обработчика для записи в файл
handler = logging.FileHandler("logs/utils.log", mode="w")
handler.setLevel(logging.DEBUG)

# Формат записи логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


def load_transactions(file_path: str) -> list[dict]:
    """Функция загружает транзакции из JSON-файла, путь к которому передается как аргумент"""
    try:
        logger.info(f"Попытка загрузить данные из файла: {file_path}")
        # Проверяю, не пустой ли файл
        with open(file_path, "r", encoding="utf-8") as f:
            first_char = f.read(1)
            if not first_char:
                logger.warning(f"Файл {file_path} пуст")
                return []
            f.seek(0)  # "Перематываю" файл к началу

            # Загружаю JSON данные
            data = json.load(f)
        result = data if isinstance(data, list) else []
        logger.info(f"Успешно загружено {len(result)} транзакций из файла {file_path}")
        return result

    except (json.JSONDecodeError, OSError, FileNotFoundError) as e:
        # Ошибка json.JSONDecodeError если файл не является корректным JSON
        # Ошибка OSError если нет доступа к файлу
        # Ошибка FileNotFoundError если файл не найден
        logger.error(f"Ошибка при загрузке данных из файла {file_path}: {e}", exc_info=True)
        return []
