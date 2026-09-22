from app.specialty.models import Specialty
from tests.test_database import TestSessionLocal


def test_create_profile_specialty(client, login, profile_id, specialty):
    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties/",
        json={"specialty_id": str(specialty.id)},
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()
    assert response.status_code == 201
    assert data["position"] == 1
    assert data["profile_id"] == profile_id
    assert data["specialty_id"] == str(specialty.id)

    # Adiciona uma segunda especialidade
    with TestSessionLocal() as session:
        new_specialty = Specialty(name="Psicologia de casal")
        session.add(new_specialty)
        session.commit()
        session.refresh(new_specialty)

    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties/",
        json={"specialty_id": str(new_specialty.id)},
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["position"] == 2

    # Adiciona uma terceira especialidade
    with TestSessionLocal() as session:
        new_specialty = Specialty(name="Psicologia de adolescente")
        session.add(new_specialty)
        session.commit()
        session.refresh(new_specialty)

    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties/",
        json={"specialty_id": str(new_specialty.id)},
        headers={"Authorization": f"Bearer {login}"},
    )

    data = response.json()

    assert response.status_code == 201
    assert data["position"] == 3


def test_add_specialty_to_another_user(client, second_login, profile_id, specialty):
    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties",
        json={"specialty_id": str(specialty.id)},
        headers={"Authorization": f"Bearer {second_login}"},
    )

    assert response.status_code == 404


def test_user_unauthenticated(client, profile_id, specialty):
    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties",
        json={"specialty_id": str(specialty.id)},
    )

    assert response.status_code == 401


def test_specialty_id_invalid_format(client, login, specialty):
    response = client.post(
        "/api/v1/profile/id-invalid-format/specialties",
        json={"specialty_id": str(specialty)},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422

def test_missing_field(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/specialties",
        json={"specialty_id": ""},
        headers={"Authorization": f"Bearer {login}"}
    )
    
    assert response.status_code == 422