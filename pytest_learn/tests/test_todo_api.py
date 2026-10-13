import pytest

url = '/items'


def test_list_items_empty(api_tester):
    response = api_tester.send_get(url)
    assert response.status_code == 200
    assert response.json() == {"items": [], "count": 0}


def test_create_item_positive(api_tester):
    response = api_tester.send_post(url, {"name": "milk", "price": 1})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "milk", "price": 1}


def test_get_real_item(api_tester):
    api_tester.create_seeded_items([{"id": 1, "name": "milk", "price": 1}])
    result = api_tester.send_get(f'{url}/1')
    assert result.status_code == 200
    assert result.json() == {"id": 1, "name": "milk", "price": 1}
    

def test_get_unreal_item(api_tester):
    api_tester.create_seeded_items([{"id": 1, "name": "milk", "price": 1}])
    result = api_tester.send_get(f'{url}/100')
    assert result.status_code == 404
    assert result.json() == {'detail': 'item not found'}
         
@pytest.mark.parametrize("enter", [
    pytest.param({"name": "milk", "price": 0}, id="0 pirce income"),
    pytest.param({"name": "milk", "price": -1}, id="-1 pirce income"),
    pytest.param({"name": "milk", "price": ''}, id="empty string price"),
    pytest.param({"name": "milk"}, id="no pirce income"),
    pytest.param({"name": "x" * 51, "price": 12}, id="51 symbols in the name")
])
def test_create_item_negative(enter, api_tester):
    result = api_tester.send_post(url, body=enter)
    assert result.status_code == 422
    assert result.json()["detail"][0]["loc"][-1] in ("price", "name")


list_items = [{"id": 1, "name": "bred", "price": 1}, {"id": 2, "name": "milk", "price": 10}, {"id": 3, "name": "orange", "price": 15}] 
@pytest.mark.parametrize("min_price, exp", [
    pytest.param(1, {"items": [{"id": 1, "name": "bred", "price": 1}, {"id": 2, "name": "milk", "price": 10}, {"id": 3, "name": "orange", "price": 15}], "count": 3}, id="filter min price 1 exp 3 items"),
    pytest.param(0, {"items": [{"id": 1, "name": "bred", "price": 1}, {"id": 2, "name": "milk", "price": 10}, {"id": 3, "name": "orange", "price": 15}], "count": 3}, id="filter min price 0 exp 3 items"),
    pytest.param(-1, {"items": [{"id": 1, "name": "bred", "price": 1}, {"id": 2, "name": "milk", "price": 10}, {"id": 3, "name": "orange", "price": 15}], "count": 3}, id="filter min price -1 exp 3 items"),
    pytest.param(2, {"items": [{"id": 2, "name": "milk", "price": 10}, {"id": 3, "name": "orange", "price": 15}], "count": 2}, id="filter min price 2 exp 2 items"),
    pytest.param(14, {"items": [{"id": 3, "name": "orange", "price": 15}], "count": 1}, id="filter min price 14 exp 1 items"),
    pytest.param(15, {"items": [{"id": 3, "name": "orange", "price": 15}], "count": 1}, id="filter min price 15 exp 1 items"),
    pytest.param(16, {"items": [], "count": 0}, id="filter min price 16 exp 0 items"),
])
def test_get_items_filter(api_tester, min_price, exp):
    api_tester.create_seeded_items(list_items)
    result = api_tester.send_get(url, f'min_price={min_price}')
    assert result.status_code == 200
    assert result.json() == exp
