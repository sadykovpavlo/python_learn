from models import Item
import pytest



def test_db_conn(db_client):
    item = Item(name='Test_name', price=10)
    db_client.add(item)
    db_client.flush()
    db_client.flush()
    inserted_item = db_client.get(Item, item.id)
    assert inserted_item.name == 'Test_name'

def test_some_post(client, db_client):
    res = client.post('/items', json={'name': "test_post", "price": 10})
    assert res.status_code == 201
    assert "id" in res.json()
    item_id = res.json()['id']
    res = client.get(f'items/{item_id}')
    assert res.json() == {'id': item_id, 'name': 'test_post', 'price': 10}
    assert db_client.query(Item).count() == 1


