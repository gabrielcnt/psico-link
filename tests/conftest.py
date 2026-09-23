import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.profile.repository import ProfileRepository
from app.shared.database.base import Base
from app.shared.database.dependencies import get_db
from app.specialty.models import Specialty
from app.specialty.repository import SpecialtyRepository
from scripts.seed_specialties import seed_specialties
from tests.test_database import TestSessionLocal, get_test_db, test_engine


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
def second_login(client, second_user):
    response = client.post(
        "api/v1/auth/login",
        data={"username": "ivmaria@email.com", "password": second_user["password"]},
    )

    token_data = response.json()
    token = token_data["access_token"]

    return token


@pytest.fixture
def second_profile_id(client, second_login):
    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "ivone maria",
            "crp": "06/97682",
            "bio": "cuidarei da sua loucura",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {second_login}"},
    )

    return response.json()["id"]


@pytest.fixture
def profile_id(client, login):
    response = client.post(
        "/api/v1/profile",
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
        "/api/v1/profile",
        json={
            "professional_name": "gabriel vieira",
            "crp": "06/46872",
            "bio": "cuidarei da sua loucura",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )
    return response.json()


@pytest.fixture
def profile_slug(profile_id):
    with TestSessionLocal() as session:
        repository = ProfileRepository(session)
        profile = repository.get_by_id(profile_id)

    return profile.slug


@pytest.fixture
def second_profile_lug(second_profile_id):
    with TestSessionLocal() as session:
        repository = ProfileRepository(session)
        profile = repository.get_by_id(second_profile_id)

    return profile.slug


@pytest.fixture
def link(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "tiktok", "url": "https://www.tiktok.com"},
        headers={"Authorization": f"Bearer {login}"},
    )

    return response.json()


@pytest.fixture
def second_link(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "facebook", "url": "https://www.facebook.com"},
        headers={"Authorization": f"Bearer {login}"},
    )

    return response.json()


@pytest.fixture
def third_link(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "instagram", "url": "https://www.instagram.com"},
        headers={"Authorization": f"Bearer {login}"},
    )

    return response.json()


@pytest.fixture
def specialty():
    with TestSessionLocal() as session:
        specialty = Specialty(name="Psicologia clínica")
        session.add(specialty)
        session.commit()
        session.refresh(specialty)

    return specialty


@pytest.fixture
def second_specialty():
    with TestSessionLocal() as session:
        specialty = Specialty(name="Psicologia infantil")
        session.add(specialty)
        session.commit()
        session.refresh(specialty)
    return specialty


@pytest.fixture
def third_specialty():
    with TestSessionLocal() as session:
        specialty = Specialty(name="Psicologia de casal")
        session.add(specialty)
        session.commit()
        session.refresh(specialty)
    return specialty


@pytest.fixture
def add_specialty(client, login, profile_id, specialty):
    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties",
        json={"specialty_id": str(specialty.id)},
        headers={"Authorization": f"Bearer {login}"},
    )
    return response


@pytest.fixture
def specialty_id(client, login, profile_id, specialty):
    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties/",
        json={"specialty_id": str(specialty.id)},
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()
    return data["specialty_id"]


@pytest.fixture
def second_specialty_id(client, login, profile_id, second_specialty):
    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties/",
        json={"specialty_id": str(second_specialty.id)},
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()
    return data["specialty_id"]


@pytest.fixture
def third_specialty_id(client, login, profile_id, third_specialty):
    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties",
        json={"specialty_id": str(third_specialty.id)},
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()
    return data["specialty_id"]


@pytest.fixture
def specialties():
    with TestSessionLocal() as session:
        seed_specialties(session)
        repository = SpecialtyRepository(session)
        list_specialties = repository.list_specialties()
    return list_specialties
