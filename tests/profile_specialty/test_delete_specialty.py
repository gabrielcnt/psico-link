from app.specialty.repository import ProfileSpecialtyRepository, SpecialtyRepository
from tests.test_database import TestSessionLocal


def test_remove_profile_specialty(client, login, profile_id, specialty_id):
    response = client.delete(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}/",
        headers={"Authorization": f"Bearer {login}"},
    )
    assert response.status_code == 204

    with TestSessionLocal() as session:
        repository = ProfileSpecialtyRepository(session)
        association = repository.get_by_profile_and_specialty(profile_id, specialty_id)

    assert association is None

    with TestSessionLocal() as session:
        repository = SpecialtyRepository(session)
        exist_specialty = repository.get_by_id(specialty_id)

    assert exist_specialty is not None


def test_association_does_not_exist(
    client, second_login, second_profile_id, specialty_id
):
    response = client.delete(
        f"/api/v1/profile/{second_profile_id}/specialties/{specialty_id}",
        headers={"Authorization": f"Bearer {second_login}"},
    )

    assert response.status_code == 404


def test_association_another_profile(client, second_login, profile_id, specialty_id):
    response = client.delete(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}",
        headers={"Authorization": f"Bearer {second_login}"},
    )

    assert response.status_code == 404


def test_user_unauthenticated(client, profile_id, specialty_id):
    response = client.delete(f"/api/v1/profile/{profile_id}/specialties/{specialty_id}")

    assert response.status_code == 401


def test_removing_specialty_does_not_affect_others_specialties(
    client,
    login,
    profile_id,
    specialty_id,
    second_specialty_id,
    third_specialty_id,
):
    response = client.delete(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 204

    with TestSessionLocal() as session:
        repository = ProfileSpecialtyRepository(session)
        second_profile_specialty = repository.get_by_profile_and_specialty(
            profile_id, second_specialty_id
        )

    assert second_profile_specialty is not None
    assert str(second_profile_specialty.specialty_id) == second_specialty_id

    with TestSessionLocal() as session:
        repository = ProfileSpecialtyRepository(session)
        third_profile_specialty = repository.get_by_profile_and_specialty(
            profile_id, third_specialty_id
        )

    assert third_profile_specialty is not None
    assert str(third_profile_specialty.specialty_id) == third_specialty_id
