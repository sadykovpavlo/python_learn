# Дрилл по маркерам + -k / -m

Работаем на уже существующих тестах. Пути — от папки pytest_learn.

---

## Задача 1 — зарегистрировать маркеры
Создай `pytest.ini` в папке pytest_learn:
```ini
[pytest]
markers =
    smoke: быстрые дымовые проверки
    db: тесты, работающие с (фейковой) БД
```
Проверь, что маркеры видны:
```bash
.venv/bin/python -m pytest --markers
```

---

## Задача 2 — повесить маркеры на тесты
- пометь `@pytest.mark.smoke` минимум ОДИН быстрый тест (например в test_orders.py)
- пометь `@pytest.mark.db` оба теста в test_fake_db.py
  (не забудь `import pytest` в test_fake_db.py — сейчас его там нет)

---

## Задача 3 — запуски-фильтры (проверь, что понимаешь разницу -m vs -k)
Прогони по очереди и посмотри, СКОЛЬКО тестов выбралось в каждом (число в итоге):

```bash
.venv/bin/python -m pytest -m smoke -v          # только smoke (по тегу)
.venv/bin/python -m pytest -m db -v             # только db (по тегу)
.venv/bin/python -m pytest -m "not db" -v       # все, кроме db
.venv/bin/python -m pytest -k "insert" -v       # по ИМЕНИ, где есть insert
.venv/bin/python -m pytest -k "fake and not seeded" -v
```

Вопрос на подумать (словами): почему `-m db` и `-k fake_db` могут дать разный набор
тестов, хотя оба «про fake_db»?

---

Когда сделаешь — покажи pytest.ini и один помеченный тест-файл.
Проверю и на этом Фаза 2 (pytest как инструмент) закрыта.
