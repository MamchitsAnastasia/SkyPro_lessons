from src import filters

SAMPLE_TRANSACTIONS = [
    {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    },
    {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    },
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 587085106,
        "state": "EXECUTED",
        "date": "2018-03-23T10:45:06.972075",
        "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Открытие вклада",
        "to": "Счет 41421565395219882431",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 214024827,
        "state": "EXECUTED",
        "date": "2018-12-20T16:43:26.929246",
        "operationAmount": {"amount": "70946.18", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 10848359769870775355",
        "to": "Счет 21969751544412966366",
    },
    {
        "id": 522357576,
        "state": "EXECUTED",
        "date": "2019-07-12T20:41:47.882230",
        "operationAmount": {"amount": "51463.70", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 48894435694657014368",
        "to": "Счет 38976430693692818358",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 596171168,
        "state": "EXECUTED",
        "date": "2018-07-11T02:26:18.671407",
        "operationAmount": {"amount": "79931.03", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Открытие вклада",
        "to": "Счет 72082042523231456215",
    },
    {
        "id": 716496732,
        "state": "EXECUTED",
        "date": "2018-04-04T17:33:34.701093",
        "operationAmount": {"amount": "40701.91", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Visa Gold 5999414228426353",
        "to": "Счет 72731966109147704472",
    },
    {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
    {
        "id": 615064591,
        "state": "CANCELED",
        "date": "2018-10-14T08:21:33.419441",
        "operationAmount": {"amount": "77751.04", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "",
        "from": "Счет 27248529432547658655",
        "to": "Счет 97584898735659638967",
    },
    {
        "id": 147815167,
        "state": "EXECUTED",
        "date": "2018-01-26T15:40:13.413061",
        "operationAmount": {"amount": "50870.71", "currency": {"name": "руб.", "code": "RUB"}},
        "description": None,
        "from": "Visa Classic 7699855375169288",
        "to": "Счет 86335492656811024678",
    },
]


def test_filter_by_description_exact_match() -> None:
    """Тестирует функцию filter_transactions_by_description
    при точном совпадении строки поиска с описанием транзакции."""
    result = filters.filter_transactions_by_description(SAMPLE_TRANSACTIONS, "Перевод организации")
    assert len(result) == 7
    assert result[0]["description"] == "Перевод организации"


def test_filter_by_description_partial_match() -> None:
    """Тестирует функцию filter_transactions_by_description
    при частичном совпадении строки поиска с описанием транзакции."""
    result = filters.filter_transactions_by_description(SAMPLE_TRANSACTIONS, "Перевод")
    assert len(result) == 10
    assert all("Перевод" in tx["description"] for tx in result)


def test_filter_by_description_case_insensitive() -> None:
    """Тестирует функцию filter_transactions_by_description на регистронезависимость"""
    result = filters.filter_transactions_by_description(SAMPLE_TRANSACTIONS, "перевод организации")
    assert len(result) == 7
    assert all("Перевод организации" in tx["description"] for tx in result)


def test_filter_by_description_no_matches() -> None:
    """Тестирует функцию filter_transactions_by_description
    при отсутствии совпадений строки поиска с описанием транзакции."""
    result = filters.filter_transactions_by_description(SAMPLE_TRANSACTIONS, "Non-existent")
    assert len(result) == 0


def test_filter_by_description_empty_search_string() -> None:
    """Тестирует функцию filter_transactions_by_description
    при отсутствии с пустой строкой поиска"""
    result = filters.filter_transactions_by_description(SAMPLE_TRANSACTIONS, "")
    assert len(result) == 0


def test_count_by_category_exact_matches() -> None:
    """Тестирует функцию count_transactions_by_category
    при точном совпадении категорий (регистронезависимый)."""
    categories = ["Перевод организации", "Открытие вклада", "Перевод со счета на счет"]
    result = filters.count_transactions_by_category(SAMPLE_TRANSACTIONS, categories)
    assert result == {"Перевод организации": 7, "Открытие вклада": 3, "Перевод со счета на счет": 2}


def test_count_by_category_case_sensitive() -> None:
    """Тестирует функцию count_transactions_by_category на регистронезависимость"""
    categories = ["перевод организации", "открытие вклада"]
    result = filters.count_transactions_by_category(SAMPLE_TRANSACTIONS, categories)
    assert result == {"перевод организации": 7, "открытие вклада": 3}


def test_count_by_category_partial_matches_not_counted() -> None:
    """Тестирует функцию count_transactions_by_category
    при частичном совпадении описаний (не учитываются при подсчете)."""
    categories = ["Перевод", "Открытие"]
    result = filters.count_transactions_by_category([], categories)
    assert result == {"Перевод": 0, "Открытие": 0}


def test_count_by_category_empty_categories() -> None:
    """Тестирует функцию count_transactions_by_category
    при пустом списке категорий (должен возвращать пустой словарь)."""
    result = filters.count_transactions_by_category(SAMPLE_TRANSACTIONS, [])
    assert result == {}


def test_count_by_category_empty_transactions() -> None:
    """Тестирует функцию count_transactions_by_category
    при пустом списке транзакций (должен возвращать нули для всех категорий)."""
    result = filters.count_transactions_by_category([], ["Перевод организации", "Открытие вклада"])
    assert result == {"Перевод организации": 0, "Открытие вклада": 0}


def test_count_by_category_with_empty_or_none_descriptions() -> None:
    """Тестирует функцию count_transactions_by_category
    при отсутствии описания у транзакций (None или пустая строка)."""
    categories = [""]
    result = filters.count_transactions_by_category(SAMPLE_TRANSACTIONS, categories)  # type: ignore[arg-type]
    assert result == {"": 0}


def test_count_by_category_mixed_case_categories() -> None:
    """Тестирует функцию count_transactions_by_category
    с категориями в разном регистре."""
    categories = ["ПЕРЕВОД ОРГАНИЗАЦИИ", "оТкРыТиЕ вКлАдА"]
    result = filters.count_transactions_by_category(SAMPLE_TRANSACTIONS, categories)
    assert result == {"ПЕРЕВОД ОРГАНИЗАЦИИ": 7, "оТкРыТиЕ вКлАдА": 3}
