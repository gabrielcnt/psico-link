def test_delete_existing_link(client, login, profile_id, link):
    response = client.delete(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 204


def test_delete_link_again(client, login, profile_id, link):
    response = client.delete(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 204

    response = client.delete(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_delete_link_other_profile(client, login, second_profile_id, link):
    response = client.delete(
        f"/api/v1/profile/{second_profile_id}/links/{link['id']}",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_delete_link_user_unauthenticated(client, profile_id, link):
    response = client.delete(f"/api/v1/profile/{profile_id}/links/{link['id']}")

    assert response.status_code == 401


def test_delete_link_without_affecting_other_links(client, login, profile_id, link):
    response_1 = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={"title": "github", "url": "https://www.github.com"},
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response_1.json()
    assert response_1.status_code == 201

    response_2 = client.delete(
        f"/api/v1/profile/{profile_id}/links/{data['id']}",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response_2.status_code == 204

    response_3 = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"title": "facebook"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response_3.status_code == 200
