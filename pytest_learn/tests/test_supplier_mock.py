"""
Моки ВНЕШНЕГО API (поставщика) — in-process, через библиотеку `responses`.
Эндпоинт GET /items/{id}/stock ходит в supplier.example.com за остатком.
В тестах реального похода НЕТ — responses перехватывает HTTP в памяти.

Работает потому, что api_tester = TestClient (in-process): внешний вызов
происходит в ЭТОМ же процессе, и responses его видит. На живом сервере так нельзя.
"""
from fastapi import HTTPException
import responses
from models import Item
from todo_api import SUPPLIER_URL
import pytest
import requests



# ─────────────────────────────────────────────────────────────
# ОБРАЗЕЦ (готовый) — поставщик ответил 200, эндпоинт вернул остаток.
# ─────────────────────────────────────────────────────────────
@responses.activate
def test_stock_ok(client, db_client):
    test_item = Item(name='carrot', price=10)
    db_client.add(test_item)
    db_client.flush()
    test_item_id = test_item.id
    # регистрируем фейковый ответ поставщика:
    responses.get(f"{SUPPLIER_URL}/stock/carrot", json={"stock": 42}, status=200)

    result = client.get(f"/items/{test_item_id}/stock")
    assert result.status_code == 200
    assert result.json() == {"id": test_item_id, "name": "carrot", "stock": 42}
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == f'{SUPPLIER_URL}/stock/carrot'


# ═══════════════════════════════════════════════════════════════════
# ТВОИ ЗАДАЧИ. Мокай ответ поставщика через responses.get(...), проверяй ветки эндпоинта.
# Смотри тело get_item_stock / fetch_supplier_stock в todo_api.py — там ветки.
# ═══════════════════════════════════════════════════════════════════

# M1. Поставщик ответил ОШИБКОЙ (напр. 500).
#     responses.get(f"{SUPPLIER_URL}/stock/carrot", status=500)
#     Что вернёт НАШ эндпоинт? (глянь except в get_item_stock) -> должно быть 502.

@responses.activate
@pytest.mark.parametrize('status_from_supplier, status_respose', [
    pytest.param(500, 502, id='Case supplier return 500'),
    pytest.param(503, 502, id='Case supplier return 503'),
    pytest.param(502, 502, id='Case supplier return 502')
])
def test_invalid_supplier_response(client, db_client, status_from_supplier, status_respose):
    test_item = Item(name='test_name', price= 700)
    db_client.add(test_item)
    db_client.flush()
    responses.get(f"{SUPPLIER_URL}/stock/{test_item.name}", status=status_from_supplier)
    res = client.get(f'/items/{test_item.id}/stock')
    assert res.status_code == status_respose
    assert res.json()['detail'] == "supplier unavailable"
 



# M2. Поставщик НЕ ОТВЕЧАЕТ (сеть упала / таймаут).
#     responses умеет симулировать сбой соединения:
#         responses.get(f"{SUPPLIER_URL}/stock/carrot", body=requests.exceptions.ConnectionError())
#     (нужен import requests сверху). Наш эндпоинт снова -> 502.

@responses.activate
def test_supplier_timeout(client, db_client):
    test_item = Item(name='test', price=100)
    db_client.add(test_item)
    db_client.flush()
    responses.get(f'{SUPPLIER_URL}/stock/{test_item.name}', body=requests.exceptions.ConnectionError())
    res = client.get(f'/items/{test_item.id}/stock')
    assert res.status_code == 502
    assert res.json()['detail'] == 'supplier unavailable'




# M3. Товара НЕТ в базе -> 404, и поставщика вообще НЕ должны дёргать.
#     Тут тонкость: если товара нет, код возвращает 404 ДО вызова поставщика.
#     Проверь status_code == 404. Подумай: надо ли тут вообще регистрировать responses.get?
def test_get_not_exist_item(client, db_client):
    test_item = Item(name='test', price=100)
    db_client.add(test_item)
    db_client.flush()
    # special step create item in DB and try find  id +100
    non_exist_item_id = test_item.id + 100 
    res = client.get(f'/items/{non_exist_item_id}/stock')
    assert res.status_code == 404
    assert res.json()['detail'] == 'item not found'


# M4 (бонус, как assert_called). Проверь, что поставщика дёрнули РОВНО раз и правильным URL:
#     после запроса -> assert len(responses.calls) == 1
#                      assert responses.calls[0].request.url == f"{SUPPLIER_URL}/stock/carrot"
#     Это HTTP-аналог твоего assert_called_once_with из мок-дрилла.
# расширил кейс 1 + полностью его переделал
