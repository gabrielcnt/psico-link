def test_change_position(client, login, profile_id, specialty_id):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}",
        json={"position": 2},
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["profile_id"] == profile_id
    assert data["position"] == 2


def test_association_not_exists(client, login, profile_id):
    profile_specialty_id = "1c4f5298-632b-4e1b-b78f-8d26451e8421"
    response = client.patch(
        f"api/v1/profile/{profile_id}/specialties/{profile_specialty_id}",
        json={"position": 5},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_association_belongs_another_profile(
    client, login, second_profile_id, specialty_id
):
    response = client.patch(
        f"/api/v1/profile/{second_profile_id}/specialties/{specialty_id}",
        json={"position": 8},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_user_unauthenticated(client, profile_id, specialty_id):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}", json={"position": 5}
    )

    assert response.status_code == 401


def test_absent_position(client, login, profile_id, specialty_id):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}",
        json={},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_none_position(client, login, profile_id, specialty_id):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}",
        json={"position": None},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_invalid_position(client, login, profile_id, specialty_id):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}",
        json={"position": "quatro"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_changing_position_does_not_change_profile_id_and_specialty_id(
    client, login, profile_id, specialty_id
):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/specialties/{specialty_id}",
        json={"position": 2},
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["profile_id"] == profile_id
    assert data["specialty_id"] == specialty_id
