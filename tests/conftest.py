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

    print(response.status_code)
    print(response.json())

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
