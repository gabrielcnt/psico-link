def test_success_create_link(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "instagram", "url": "https://www.instagram.com"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 201
    assert response.json()["position"] == 1

    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "facebook", "url": "https://www.facebook.com/?locale=pt_BR"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.json()["position"] == 2

    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "tiktok", "url": "https://www.tiktok.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.json()["position"] == 3


def test_duplicity_title_link(client, profile_id, login):
    response_1 = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={"title": "tiktok", "url": "https://www.tiktok.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response_1.status_code == 201

    response_2 = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={"title": "tiktok", "url": "https://www.tiktok.com/234"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response_2.status_code == 409


def test_duplicity_url_link(client, profile_id, login, second_user):
    response_1 = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "tiktok 1", "url": "https://www.tiktok.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response_1.status_code == 201

    response_2 = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "tiktok 2", "url": "https://www.tiktok.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response_2.status_code == 409


def test_allow_identical_title_links_differents_profiles(
    client, login, second_login, profile_id, second_profile_id
):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "tiktok", "url": "https://www.tiktok.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 201

    response = client.post(
        f"/api/v1/profile/{second_profile_id}/links/",
        json={"title": "tiktok", "url": "https://www.tiktok.com/1233"},
        headers={"Authorization": f"Bearer {second_login}"},
    )

    assert response.status_code == 201


def test_allow_identical_url_links_differents_profiles(
    client, login, second_login, profile_id, second_profile_id
):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "tiktok 1", "url": "https://www.tiktok.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 201

    response = client.post(
        f"/api/v1/profile/{second_profile_id}/links/",
        json={"title": "tiktok 2", "url": "https://www.tiktok.com/"},
        headers={"Authorization": f"Bearer {second_login}"},
    )

    assert response.status_code == 201
