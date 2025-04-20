import os

import requests
from dotenv import load_dotenv

load_dotenv("../keys.env")
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")

BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: dict) -> float:
    """Функция переводит валюту в RUB, запрашивая курсы на стороннем ресурсе."""
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency = operation_amount.get("currency", {}).get("code", "RUB").upper()

    if currency == "RUB":
        return amount

    try:
        response = requests.get(
            BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY}, timeout=10
        )
        response.raise_for_status()
        rates = response.json().get("rates", {})
        rate = rates.get("RUB", 1)
        return float(amount) * float(rate)

    except Exception as e:
        raise ValueError(f"Ошибка конвертации валюты: {e}")
