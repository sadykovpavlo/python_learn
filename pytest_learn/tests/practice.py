"""Простые функции под тест — для закрепляющего дрилла.
Каждая маленькая, но со своими граничными и негативными случаями."""


# --- A. Агрегация в цикле (dict-аккумулятор) ---
def count_by_status(tickets: list[dict]) -> dict[str, int]:
    """Считает, сколько тикетов в каждом статусе.
    [{'id':1,'status':'open'}, {'id':2,'status':'open'}, {'id':3,'status':'closed'}]
    -> {'open': 2, 'closed': 1}. Пустой список -> {}."""
    counts: dict[str, int] = {}
    for t in tickets:
        status = t["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


# --- B. Разбор строки (split + strip + фильтр пустых + lower) ---
def parse_tags(raw: str) -> list[str]:
    """'Python, API ,,  pytest ' -> ['python', 'api', 'pytest'].
    Разбить по запятой, обрезать пробелы, выкинуть пустые, привести к нижнему регистру."""
    result: list[str] = []
    for part in raw.split(","):
        cleaned = part.strip().lower()
        if cleaned:
            result.append(cleaned)
    return result


# --- C. Валидация + категоризация (тут живут boundary/negative кейсы) ---
def classify_age(age: int) -> str:
    """Категория по возрасту. Границы важны!
    0..17 -> 'minor', 18..64 -> 'adult', 65..150 -> 'senior'.
    age < 0 или age > 150 -> ValueError."""
    if age < 0 or age > 150:
        raise ValueError(f"age out of range: {age}")
    if age < 18:
        return "minor"
    if age < 65:
        return "adult"
    return "senior"


# --- D. Внешний вызов (для моков) ---
def fetch_profile(user_id: int) -> dict:
    """'Внешний' сервис профилей. В тестах мокаем."""
    raise RuntimeError("Реальный сетевой вызов за профилем! В тесте так быть не должно.")


def enrich_user(user_id: int) -> dict:
    """Тянет профиль через fetch_profile и оборачивает в ответ.
    Если сервис недоступен (TimeoutError) — не падает, помечает статус 'unavailable'."""
    try:
        profile = fetch_profile(user_id)
    except TimeoutError:
        return {"id": user_id, "status": "unavailable", "profile": None}
    return {"id": user_id, "status": "ok", "profile": profile}
