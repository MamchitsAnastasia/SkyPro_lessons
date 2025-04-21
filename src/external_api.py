import logging
import os

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

os.makedirs("logs", exist_ok=True)

# Настройка обработчика для записи в файл
handler = logging.FileHandler("logs/external_api.log", mode="w", encoding="utf-8")
handler.setLevel(logging.ERROR)

# Формат записи логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

load_dotenv("../keys.env")
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: dict) -> float:
    """Функция переводит валюту в RUB, запрашивая курсы на стороннем ресурсе.
    Возвращает 0.0 при любых ошибках."""
    try:
        operation_amount = transaction.get("operationAmount", {})
        currency_data = operation_amount.get("currency", {})

        try:
            amount = float(operation_amount.get("amount", 0))
        except (ValueError, TypeError) as e:
            logger.error(f"Ошибка преобразования суммы: {e}")
            return 0.0

        currency = currency_data.get("code", "RUB").upper()

        if currency == "RUB":
            return amount

        if not API_KEY and not os.environ.get("TESTING"):
            logger.error("API ключ не найден")
            return 0.0

        try:
            response = requests.get(
                BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY}, timeout=10
            )
            response.raise_for_status()

            rates = response.json().get("rates", {})
            rate = rates.get("RUB", 1)
            return float(amount) * float(rate)

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка API: {e}")
            return 0.0

        except (ValueError, KeyError) as e:
            logger.error(f"Ошибка обработки ответа API: {e}")
            return 0.0

    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")
        return 0.0
