# SQLAlchemy + Alembic — куда что писать

> Справочник по структуре, не решение задачи. Команды/расположение файлов — отсюда,
> саму модель `Item` и логику эндпоинтов пишешь сам.

## Структура директорий (куда класть файлы)

```
pytest_learn/
├── tests/
│   ├── database.py       ← НОВЫЙ файл: engine + SessionLocal + get_db (как src/db/session.py в mem_hunter)
│   ├── models.py         ← НОВЫЙ файл: SQLAlchemy-модели (Base, Item) — твой класс сюда
│   ├── todo_api.py        (существующий — сюда допишешь Depends(get_db) в эндпоинты)
│   └── config.py          (существующий Settings — допишешь database_url)
├── alembic/               ← СОЗДАСТСЯ командой `alembic init` (см. ниже), не пишешь руками
│   ├── versions/          ← сюда Alembic кладёт сгенерированные миграции (авто)
│   └── env.py             ← нужно поправить ОДНУ строку (см. ниже)
└── alembic.ini             ← СОЗДАСТСЯ той же командой, настройка — одна строка
```

## 1. `tests/database.py` — engine и сессия (откуда брать пример: `mem_hunter/src/db/session.py`, но SYNC-версия)

Сигнатура, которую нужно заполнить (это НЕ решение, только форма — что от чего зависит):
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine("ПОДСТАВИТЬ: URL из Settings")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    # setup → yield → teardown, тот же паттерн что db-фикстура в conftest.py
    ...
```

## 2. `tests/models.py` — твоя модель (пример формы, см. `mem_hunter/src/db/models.py` → класс `SmartWallet` для стиля)

```python
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Item(Base):
    __tablename__ = "items"
    # дальше сам: id, name, price — какие типы/mapped_column?
```

## 3. Установка Alembic (уже сделано) + инициализация

Команда (выполнить ОДИН раз в `pytest_learn/`):
```bash
.venv/bin/alembic init alembic
```
Это САМО создаст папку `alembic/` + файл `alembic.ini` — не создавай их руками.

## 4. Что поправить ПОСЛЕ `alembic init` (две точки конфигурации)

- **`alembic.ini`** — строка `sqlalchemy.url = ...` — вписать URL твоей тестовой Postgres
  (`postgresql://postgres:postgres@localhost:6454/postgres` — порт из твоего `docker-compose.yaml`).
- **`alembic/env.py`** — строка `target_metadata = None` — заменить на `target_metadata = Base.metadata`
  (импортировав `Base` из `tests/database.py`) — это и есть связь "Alembic, смотри на ЭТИ модели,
  чтобы понять что менять".

## 5. Команды генерации/применения миграции (после того как модель написана)

```bash
.venv/bin/alembic revision --autogenerate -m "add items table"   # сгенерировать миграцию из модели
.venv/bin/alembic upgrade head                                    # применить к реальной БД
```

## Откуда вообще брать знание (если захочешь читать сам)

- SQLAlchemy 2.0 ORM Quickstart (официальная документация) — `Mapped`/`mapped_column`, то же,
  что ты уже видел в `mem_hunter`.
- Alembic Tutorial (официальная документация) — `autogenerate`, `env.py`.
- Твой же `mem_hunter/src/db/models.py` и `session.py` — живой пример (async-версия, но структура 1:1).
