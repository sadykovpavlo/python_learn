# Закрепляющий дрилл: питон-идиомы + pytest (моки/фикстуры/parametrize/маркеры)

SUT: `tests/practice.py` (4 функции). Тесты пиши в `tests/test_practice.py`.
Пути — от папки pytest_learn. Запуск:
```bash
.venv/bin/python -m pytest tests/test_practice.py -v
```

ГЛАВНЫЙ НАВЫК из твоей целевой вакансии: **сам придумай сценарии** для каждой функции —
positive / negative / boundary / edge. Перед кодом кейсов ответь себе: какие входы
«ломают» функцию или лежат на границе? Это важнее, чем синтаксис.

---

## Блок A — count_by_status  (цикл-агрегация)
Техника: обычный assert + parametrize + фикстура с данными.
1. Фикстура `tickets` с 3–4 тикетами разных статусов.
2. Тест: `count_by_status(tickets)` возвращает верный словарь.
3. Через `@pytest.mark.parametrize` покрой хотя бы:
   - обычный случай,
   - **edge: пустой список** -> `{}`,
   - edge: все тикеты одного статуса.

## Блок B — parse_tags  (строки/фильтрация)
Техника: parametrize, дизайн граничных входов.
Придумай кейсы сам, обязательно включи:
- обычная строка `'Python, API, pytest'`,
- **лишние пробелы и пустые куски** `' a ,, b ,  '`,
- **edge: пустая строка** `''` -> `[]`,
- edge: строка только из запятых `',,,'` -> `[]`,
- регистр: `'PyTest'` -> `'pytest'`.

## Блок C — classify_age  (валидация + boundary — это ядро вакансии!)
Техника: parametrize + `pytest.raises`.
Обязательно покрой ГРАНИЦЫ (не серединки диапазонов):
- 0, 17, 18, 64, 65, 150  (правильные категории на самых краях)
- **negative: -1 и 151** должны кидать `ValueError` — лови через `with pytest.raises(ValueError):`
Подумай: почему тест именно на 17 и 18 важнее, чем на 5 и 40?

## Блок D — enrich_user  (моки: return_value + side_effect)
Техника: `mocker.patch` (патчь ТАМ, где используется -> `practice.fetch_profile`).
1. Happy path: замокай `fetch_profile` через `return_value={"name": "Alice"}`,
   проверь что `enrich_user(1)` вернул `{"id":1,"status":"ok","profile":{"name":"Alice"}}`
   и что мок вызван один раз с `1`.
2. Сервис упал: `side_effect=TimeoutError`, проверь что вернулось
   `{"id":1,"status":"unavailable","profile":None}` (код НЕ упал).

---

## Блок E — ЧИСТЫЙ ПИТОН (пишешь функцию САМ, потом тест) — это про "strong Python"
Тут я НЕ даю готовую функцию. Реализуй каждую в `tests/practice_e.py` с аннотациями типов,
используя ИМЕННО указанный инструмент (в этом весь смысл — гонять built-ins до автоматизма).
Потом хотя бы для 3 из них напиши parametrize-тесты (обязательно с edge: пустой вход).

1. `unique_tags(raws: list[str]) -> list[str]`
   `['Py','api','py','API']` -> `['api','py']`  (уникальные, lower, отсортированы)
   Инструмент: **set** (или set-comprehension) + **sorted**.

2. `most_common_status(tickets: list[dict]) -> str`
   вернуть статус, который встречается чаще всего.
   Инструмент: **collections.Counter** + **.most_common(1)**.

3. `all_paid(orders: list[dict]) -> bool` и `any_refunded(orders: list[dict]) -> bool`
   Инструмент: **all()** / **any()** + генераторное выражение внутри
   (тут генвыражение УМЕСТНО — не путать с прошлой ошибкой, где нужен был for).

4. `richest(orders: list[dict]) -> str`
   имя покупателя с максимальным amount.
   Инструмент: **max(..., key=lambda ...)**.

5. `numbered(titles: list[str]) -> list[str]`
   `['a','b']` -> `['1. a', '2. b']`.
   Инструмент: **enumerate(start=1)** + f-string.

6. `names_to_scores(names: list[str], scores: list[int]) -> dict[str,int]`
   `['a','b'], [10,20]` -> `{'a':10,'b':20}`.
   Инструмент: **zip** + **dict-comprehension**.

7. (со звёздочкой, новое — можешь пропустить или спросить объяснение)
   `running_total(nums: list[int])` — ГЕНЕРАТОР через `yield`, отдающий нарастающий итог:
   `[10,20,5]` -> по одному 10, 30, 35. Инструмент: функция с **yield** (не return).

Вопрос на подумать: в п.3 генвыражение — ок, а в прошлом дрилле с insert — нет. В чём разница?

---

## Маркеры (закрепим прошлую тему)
Помечай быстрые тесты `@pytest.mark.smoke`. Потом прогони `-m smoke` и убедись,
что выбираются только они. (маркер smoke уже зарегистрирован в pytest.ini)

---

Когда сделаешь — покажи `tests/test_practice.py`. Разберём и стиль, и ПОЛНОТУ
покрытия (не пропустил ли ты негативные/граничные кейсы — за этим на собесе следят).
