# FastAPI `dependency_overrides` — шпаргалка

## Три правила, которые легко перепутать

| Правило | Неправильно | Правильно |
|---|---|---|
| Ключ — та же функция, что в `Depends(...)` у эндпоинта | `app.dependency_overrides[get_db_test]` (своя функция ключом) | `app.dependency_overrides[get_db]` (импортирована ИЗ `database.py`, та же, что в эндпоинте) |
| Значение — ФУНКЦИЯ, не готовый объект | `app.dependency_overrides[get_db] = db_client` | `app.dependency_overrides[get_db] = override_get_db` |
| Без скобок — не вызывать | `= override_get_db()` (создаёт ОДИН генератор, истощится после 1-го запроса) | `= override_get_db` (ссылка на функцию — FastAPI сам вызовет на каждый запрос) |

## Почему именно так (в одной фразе на каждое)

- **Ключ** — FastAPI ищет в словаре ТОТ ЖЕ объект-функцию, что видит в сигнатуре эндпоинта
  (`Depends(get_db)`). Своё имя для ключа — бессмысленно, FastAPI его там не ищет.
- **Значение-функция** — потому что FastAPI сам ЗОВЁТ то, что лежит в overrides, как и настоящую
  `get_db`. Объект (`Session`) вызвать нельзя — `TypeError`.
- **Без `()`** — генератор истощается после одного использования. FastAPI должен вызывать СВЕЖИЙ
  экземпляр на КАЖДЫЙ запрос — для этого ему нужна сама функция, а не уже готовый (и использованный)
  результат её вызова.

## Форма override-функции (минимальная)

```python
def override_get_db():
    yield db_client   # просто отдать готовую тестовую сессию, БЕЗ commit — это не замена логики,
                        # а просто "откуда брать сессию"
```

## Полная сборка (контекст)

```python
from todo_api import app
from database import get_db

@pytest.fixture
def client(db_client):
    def override_get_db():
        yield db_client

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```
