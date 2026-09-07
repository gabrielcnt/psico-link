import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.shared.database.base import Base
from app.shared.database.dependencies import get_db
from tests.test_database import get_test_db, test_engine


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def client():

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(client):
    response = client.post(
        "api/v1/auth/register",
        json={
            "name": "gabriel",
            "email": "gabriel@email.com",
            "password": "12345678",
        },
    )

    data = response.json()
    password = "12345678"

    return {"email": data["email"], "password": password}


@pytest.fixture
def second_user(client):
    response = client.post(
        "api/v1/auth/register",
        json={
            "name": "ivone maria",
            "email": "ivmaria@email.com",
            "password": "12345678",
        },
    )

    data = response.json()
    password = "12345678"

    return {"email": data["email"], "password": password}


@pytest.fixture
def login(client, user):
    response = client.post(
        "api/v1/auth/login",
        data={"username": user["email"], "password": user["password"]},
    )

    token_data = response.json()
    token = token_data["access_token"]

    return token


@pytest.fixture
def login(client, second_user):
    response = client.post(
        "api/v1/auth/login",
        data={"username": second_user["email"], "password": second_user["password"]},
    )

    token_data = response.json()
    token = token_data["access_token"]

    return token


@pytest.fixture
def profile_id(client, login):
    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "gabriel vieira",
            "crp": "06/46872",
            "bio": "cuidarei da sua loucura",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    data = response.json()

    return data["id"]


@pytest.fixture
def profile(client, login):
    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "gabriel vieira",
            "crp": "06/46872",
            "bio": "cuidarei da sua loucura",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    print(response.json())

    return response.json()
