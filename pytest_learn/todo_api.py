"""
Учебный REST API на FastAPI — items store в памяти.
Твоя задача — ТЕСТИРОВАТЬ его через TestClient, а не менять код.
Читай тело эндпоинтов: где какой статус-код возвращается — это и есть ветки,
которые надо покрыть тестами (твоя тренируемая слабая зона).
"""

import requests
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Item

app = FastAPI()

# Адрес ВНЕШНЕГО сервиса поставщика (в тестах реально туда ходить нельзя — мокаем).
SUPPLIER_URL = "https://supplier.example.com"


class ItemIn(BaseModel):
    """Тело запроса на создание. Pydantic сам валидирует -> 422 если не так."""

    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)  # gt=0 -> цена строго больше 0


def _to_dict(item: Item) -> dict:
    return {"id": item.id, "name": item.name, "price": item.price}


@app.get("/items")
def list_items(min_price: float | None = None, db: Session = Depends(get_db)):
    """GET /items  или  /items?min_price=100 — вернуть все / отфильтрованные."""
    query = db.query(Item)
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    result = [_to_dict(item) for item in query.all()]
    return {"items": result, "count": len(result)}


@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """GET /items/5 — 200 с товаром или 404, если нет."""
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return _to_dict(item)


@app.post("/items", status_code=201)
def create_item(item: ItemIn, db: Session = Depends(get_db)):
    """POST /items — создать. 201 + созданный объект. Кривое тело -> 422 (Pydantic)."""
    record = Item(name=item.name, price=item.price)
    db.add(record)
    db.flush()  # получить сгенерированный id без полного commit (commit делает get_db)
    db.refresh(record)
    return _to_dict(record)


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """DELETE /items/5 — 204 без тела, или 404 если нечего удалять."""
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    db.delete(item)


def fetch_supplier_stock(name: str) -> int:
    """Идёт во ВНЕШНИЙ API поставщика за остатком на складе. Это ТА функция,
    чей HTTP-вызов будем мокать в тестах (реально в supplier.example.com не ходим)."""
    response = requests.get(f"{SUPPLIER_URL}/stock/{name}", timeout=5)
    response.raise_for_status()  # не-2xx -> кинет requests.HTTPError
    return response.json()["stock"]


@app.get("/items/{item_id}/stock")
def get_item_stock(item_id: int, db: Session = Depends(get_db)):
    """GET /items/5/stock — вернуть остаток товара, спросив у внешнего поставщика.
    Ветки: 404 если товара нет; 502 если поставщик недоступен/ответил ошибкой."""
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    try:
        stock = fetch_supplier_stock(item.name)
    except requests.RequestException:
        # поставщик лёг / таймаут / вернул ошибку -> отдаём 502 наружу
        raise HTTPException(status_code=502, detail="supplier unavailable")
    return {"id": item_id, "name": item.name, "stock": stock}
