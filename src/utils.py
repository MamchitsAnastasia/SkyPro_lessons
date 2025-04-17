import json


def load_transactions(file_path: str) -> list[dict]:
    """Функция загружает транзакции из JSON-файла, путь к которому передается как аргумент"""
    try:
        # Проверяю, не пустой ли файл
        with open(file_path, "r", encoding="utf-8") as f:
            first_char = f.read(1)
            if not first_char:
                return []
            f.seek(0)  # "Перематываю" файл к началу

            # Загружаю JSON данные
            data = json.load(f)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError, FileNotFoundError):
        # Ошибка json.JSONDecodeError если файл не является корректным JSON
        # Ошибка OSError если нет доступа к файлу
        # Ошибка FileNotFoundError если файл не найден
        return []
