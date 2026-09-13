def test_update_title(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}/",
        json={"title": "facebook"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200


def test_update_url(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}/",
        json={"url": "https://www.facebook.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200


def test_update_position(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"position": 2},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200


def test_update_many_fields(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"title": "facebook", "url": "https://www.facebook.com", "position": 3},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200


def test_update_none_field(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"title": "", "url": ""},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_update_duplicate_title(client, login, profile_id, link):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links/",
        json={"title": "facebook", "url": "https://wwww.facebook.com"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 201

    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"title": "facebook"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 409


def test_update_duplicate_url(client, login, profile_id, link):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={
            "title": "intagram",
            "url": "https://www.instagram.com",
        },
        headers={"Authorization": f"Bearer {login}"},
    )
    print(response.json())
    assert response.status_code == 201

    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={
            "url": "https://www.instagram.com",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 409


def test_keep_title(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"title": "tiktok"},
        headers={"Authorization": f"Bearer {login}"},
    )
    assert response.status_code == 200


def test_keep_url(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"url": "https://www.tiktok.com"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200


def test_link_not_found(client, login, profile_id):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/1c4f5298-632b-4e1b-b78f-8d26451e0481",
        json={"title": "twitter", "url": "https://www.twitter.com"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_link_belongs_another_profile(client, login, second_profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{second_profile_id}/links/{link['id']}",
        json={"title": "facebook"},
        headers={"Authorization": f"Bearer {login}"},
    )
    assert response.status_code == 404


def test_user_unauthenticated(client, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}", json={"title": "github"}
    )

    assert response.status_code == 401


def test_title_too_short(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"title": "tu"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_invalid_url(client, login, profile_id, link):
    response = client.patch(
        f"/api/v1/profile/{profile_id}/links/{link['id']}",
        json={"url": "url-invalida"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422
