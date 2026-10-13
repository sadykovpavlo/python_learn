"""Код под тест (SUT) с ВНЕШНИМ вызовом get_exchange_rate — его мокаем в тестах."""


def get_exchange_rate(currency: str) -> float:
    """'Внешний' сервис курсов валют. В реальности лез бы по сети за курсом.
    В тестах мы его мокаем: подставляем нужный курс (return_value)
    или заставляем упасть с таймаутом (side_effect)."""
    raise RuntimeError("Реальный сетевой вызов за курсом! В тесте так быть не должно.")


def convert_price(amount: float, currency: str) -> dict:
    """Конвертирует amount из currency в UAH по внешнему курсу.
    Если сервис курсов недоступен (TimeoutError) — не падает,
    а возвращает результат с пометкой об ошибке."""
    try:
        rate = get_exchange_rate(currency)
    except TimeoutError:
        return {"currency": currency, "uah": None, "error": "rate_unavailable"}
    return {"currency": currency, "uah": round(amount * rate, 2), "error": None}
