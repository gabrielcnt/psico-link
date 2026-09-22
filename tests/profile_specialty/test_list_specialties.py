from app.specialty.repository import ProfileSpecialtyRepository
from tests.test_database import TestSessionLocal


def test_list_profile_specialties(
    client, login, profile_id, specialty_id, second_specialty_id, third_specialty_id
):
    response = client.get(
        f"/api/v1/profile/{profile_id}/specialties/",
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert isinstance(data, list)

    assert len(data) == 3
    assert data[0]["specialty_id"] == specialty_id
    assert data[1]["specialty_id"] == second_specialty_id
    assert data[2]["specialty_id"] == third_specialty_id

    assert data[0]["profile_id"] == profile_id
    assert data[1]["profile_id"] == profile_id
    assert data[2]["profile_id"] == profile_id

    assert data[0]["position"] == 1
    assert data[1]["position"] == 2
    assert data[2]["position"] == 3


def test_positional_ordering(
    client, login, profile_id, specialty_id, second_specialty_id, third_specialty_id
):
    with TestSessionLocal() as session:
        repository = ProfileSpecialtyRepository(session)

        # psicologia clinica
        get_specialty = repository.get_by_profile_and_specialty(
            profile_id, specialty_id
        )
        get_specialty.position = 3
        update_specialty = repository.update(get_specialty)
        clinical_psychology = update_specialty

        # psicologia infantil
        get_specialty = repository.get_by_profile_and_specialty(
            profile_id, second_specialty_id
        )
        get_specialty.position = 1
        update_specialty = repository.update(get_specialty)
        child_psychology = update_specialty

        # psicologia de casal
        get_specialty = repository.get_by_profile_and_specialty(
            profile_id, third_specialty_id
        )
        get_specialty.position = 2
        update_specialty = repository.update(get_specialty)
        couples_psychology = update_specialty

        response = client.get(
            f"/api/v1/profile/{profile_id}/specialties",
            headers={"Authorization": f"Bearer {login}"},
        )

        data = response.json()
        print(data)
        assert response.status_code == 200

        assert data[0]["specialty_id"] == str(child_psychology.specialty_id)
        assert data[1]["specialty_id"] == str(couples_psychology.specialty_id)
        assert data[2]["specialty_id"] == str(clinical_psychology.specialty_id)


def test_profile_with_no_specialties(client, login, profile_id):
    response = client.get(
        f"/api/v1/profile/{profile_id}/specialties",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_another_users_profile(client, second_login, profile_id):
    response = client.get(
        f"/api/v1/profile/{profile_id}/specialties",
        headers={"Authorization": f"Bearer {second_login}"},
    )

    assert response.status_code == 404


def test_profile_not_found(client, login):
    response = client.get(
        "/api/v1/profile/4f7e2b19-c38a-4d62-9e51-85af40ef39b2/specialties",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_user_unauthenticated(client, profile_id):
    response = client.get(f"/api/v1/profile/{profile_id}/specialties")

    assert response.status_code == 401
