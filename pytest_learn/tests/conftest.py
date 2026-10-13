import pytest
import pytest_asyncio
import requests
import asyncio
import httpx
from config import Settings
from fake_db import FakeDB
from fastapi.testclient import TestClient
from todo_api import app
from database import engine, get_db
from sqlalchemy.orm import Session

@pytest.fixture
def client(db_client):
    def overvide_get_db():
        yield db_client
    app.dependency_overrides[get_db] = overvide_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def db_client():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    transaction.rollback()
    connection.close()



@pytest.fixture(scope="session")
def api_client(base_url):
    return LiveApiTester(base_url)

@pytest_asyncio.fixture(scope='session',loop_scope='session')
async def async_api_client(base_url):
    tester = AsyncApiTester(base_url=base_url)
    yield tester
    await tester.client.aclose()
        


@pytest.fixture(scope="session")
def settings(env):
    return Settings(_env_file=f".env.{env}")


@pytest.fixture(scope="session")
def base_url(settings):
    return settings.base_url


@pytest.fixture
def clean_up_data(base_url):
    ids = []
    yield ids
    for item_id in ids:
        requests.delete(f"{base_url}/items/{item_id}")


@pytest.fixture
def db():
    conn = FakeDB()
    conn.connect()
    yield conn
    conn.close()


@pytest.fixture
def seeded_fake_db(db):
    test_users = [{"id": 1, "name": "alice"}, {"id": 2, "name": "bob"}]
    for user in test_users:
        db.insert(user)
    return db


class ApiTester:
    def __init__(self, app, ITEMS, _next_id):
        self.app = app
        self.ITEMS = ITEMS
        self._next_id = _next_id
        self.client = TestClient(self.app)

    def send_get(self, url, param=None):
        if param:
            result = self.client.get(f"{url}?{param}")
            return result
        result = self.client.get(url)
        return result

    def send_post(self, url, body):
        result = self.client.post(url, json=body)
        return result

    def send_delete(self, url):
        result = self.client.delete(url)
        return result

    def create_seeded_items(self, values: list[dict[str, str | int]]):
        self.ITEMS.clear()
        first_id = 1
        for value in values:
            self.ITEMS[first_id] = value
            first_id += 1
        self._next_id["value"] = first_id


class LiveApiTester:
    def __init__(self, base_url):
        self.base_url = base_url

    def clean_up_url(self, url: str) -> str:
        symbols = (";", "<", ">", ".", ",", "?")
        cleaned_url = [u for u in url if u not in symbols]
        if cleaned_url[0] == "/":
            cleaned_url.pop(0)
        if cleaned_url[-1] == "/":
            cleaned_url.pop(-1)
        return "".join(cleaned_url)

    def send_get(self, url, params: str = None):
        url = self.clean_up_url(url)
        if params:
            resposne = requests.get(f"{self.base_url}/{url}?{params}")
            return resposne
        resposne = requests.get(f"{self.base_url}/{url}")
        return resposne

    def send_post(self, url, requst_body):
        url = self.clean_up_url(url)
        response = requests.post(f"{self.base_url}/{url}", json=requst_body)
        return response

    def send_delete(self, url):
        url = self.clean_up_url(url)
        response = requests.delete(f"{self.base_url}/{url}")
        return response


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="local", help="local | ci")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


class AsyncApiTester:
    def __init__(self, base_url):
        self.client = httpx.AsyncClient(base_url=base_url)

   
    async def send_get(self, url: str, params= None):
        if params:
            response = await self.client.get(f'{url}?{params}')
            return response
        response = await self.client.get(f'{url}')
        return response


    async def send_post(self, url, body=None):
        if body:
            response = await self.client.post(url, json=body)
            return response
        response = await self.client.post(url)
        return response
        
    async def send_delete(self, url):
        response = await self.client.delete(url)
        return response

                

