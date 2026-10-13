import pytest
import httpx
from async_drill import return_name_sleep, validate_age


@pytest.mark.asyncio
async def test_return_name_sleep():
    res = await return_name_sleep("pasha", 2)
    assert res == "Hello Pasha"


@pytest.mark.parametrize("entered, expected", [
    pytest.param(-1, "Age cant be less than 0", id="Boundary -1"),
    pytest.param(-1000, "Age cant be less than 0", id="Simple negative -1000"),
])

@pytest.mark.asyncio
async def test_validatior_age_negative(entered, expected):
    with pytest.raises(ValueError, match=expected):
         await validate_age(entered)


# @pytest.mark.asyncio
# async def test_post_request():
#     async with httpx.AsyncClient(base_url = 'http://127.0.0.1:8000') as client:
#         response =  await client.post(url='/items', json={"name": "test item", "price": 10})
#         assert response.status_code == 201
#         item_id = response.json()['id']
#         response = await client.get(url=f'/items/{item_id}')
#         assert response.status_code == 200
#         assert response.json()['id'] == item_id
#         assert response.json()['name'] == "test item"


@pytest.mark.asyncio
async def test_async_post_request(async_api_client):
    response = await async_api_client.send_post(url='/items', body={"name": "test item", "price": 10})
    assert response.status_code == 201
    item_id = response.json()['id']
    response = await async_api_client.send_get(f'/items/{item_id}')
    assert response.status_code == 200
    assert response.json()['name'] == "test item"
    assert response.json()['id'] == item_id