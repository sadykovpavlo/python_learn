"""
Тесты против ЖИВОГО сервера (uvicorn), по настоящему HTTP через requests.
Перед запуском сервер должен быть поднят:
    PYTHONPATH=tests .venv/bin/uvicorn todo_api:app --port 8000
Запуск тестов:
    .venv/bin/python -m pytest tests/test_live_api.py -v

ВАЖНО: сервер — отдельный процесс. ITEMS.clear() тут НЕ РАБОТАЕТ (чужая память).
Данные готовим/чистим ТОЛЬКО через API (POST/DELETE).
"""

# BASE_URL = "http://127.0.0.1:8000"

# ─────────────────────────────────────────────────────────────
# ОБРАЗЕЦ (готовый) — GET по живому серверу.
# ─────────────────────────────────────────────────────────────

def test_live_list_items(api_client):
    response = api_client.send_get('/items')
    assert response.status_code == 200
    # тело НЕ проверяем на пустоту — сервер мог накопить данные от прошлых тестов
    assert "items" in response.json()
    assert "count" in response.json()


# ═══════════════════════════════════════════════════════════════════
# ТВОИ ЗАДАЧИ. Всё через requests + BASE_URL. Response API тот же (.status_code/.json()).
# ═══════════════════════════════════════════════════════════════════

# R1. POST создаёт товар на ЖИВОМ сервере.
#     requests.post(f"{BASE_URL}/items", json={...})  -> 201, проверь name/price в теле.
#     Внимание: id теперь НЕ угадаешь (сервер копил данные) — не ассёрть конкретный id,
#     проверь что "id" ЕСТЬ в ответе (assert "id" in body).

def test_create_items(api_client, clean_up_data):
    response = api_client.send_post('/items', requst_body={'name': 'carrot', 'price': 10})
    body = response.json()
    clean_up_data.append(body['id'])
    assert response.status_code == 201
    assert body['name'] == 'carrot'
    assert body['price'] == 10
    
    


# R2. Полный жизненный цикл через API (интеграционный сценарий — то, что любят на собесе):
#     1) POST создать товар -> запомни id из ответа (created = response.json(); item_id = created["id"])
#     2) GET /items/{id} -> 200, тот же товар
#     3) DELETE /items/{id} -> 204
#     4) GET /items/{id} снова -> теперь 404 (удалён)
#     Это самопроверяющийся тест: сам создал, сам проверил, сам за собой убрал.

# clean_up_data добавил чисто для страховки
def test_life_cycle_items(api_client, clean_up_data):
    response = api_client.send_post('/items', requst_body={'name': 'test', 'price': 10})
    body = response.json()
    item_id = body['id']
    clean_up_data.append(item_id)
    assert response.status_code == 201
    assert body['name'] == 'test'
    assert body['price'] == 10
    response = api_client.send_get(f'/items/{item_id}')
    body = response.json()
    assert response.status_code == 200
    assert body['name'] == 'test'
    assert body['price'] == 10
    response = api_client.send_delete(f'/items/{item_id}')
    assert response.status_code == 204
    response = api_client.send_get(f'/items/{item_id}')
    assert response.status_code == 404


# R3. DELETE несуществующего -> 404 (тело detail "item not found").
def test_delete_not_exist_item(api_client):
    response = api_client.send_delete('/items/404')
    assert response.status_code == 404
    assert response.json() == {'detail': 'item not found'}