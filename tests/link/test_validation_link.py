def test_validation_title_link(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={"title": "fb", "url": "https://www.facebook.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_validation_url_link(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={"title": "facebook", "url": "site-do-facebook"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_title_field_missing(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={"title": "", "url": "https://www.facebook.com/"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_url_field_missing(client, login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={
            "title": "facebook",
            "url": "",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422
