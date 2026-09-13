def test_user_without_token(client, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={
            "title": "instagram",
            "url": "https://www.instagram.com/",
        },
    )

    assert response.status_code == 401


def test_user_not_found_profile(client, login):

    response = client.post(
        "/api/v1/profile/2190ac56-5066-4f89-8722-7d90da38557b/links",
        json={
            "title": "instagram",
            "url": "https://www.instagram.com/",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_user_cannot_access_another_profile(client, second_login, profile_id):
    response = client.post(
        f"/api/v1/profile/{profile_id}/links",
        json={
            "title": "instagram",
            "url": "https://www.instagram.com/",
        },
        headers={"Authorization": f"Bearer {second_login}"},
    )

    assert response.status_code == 404