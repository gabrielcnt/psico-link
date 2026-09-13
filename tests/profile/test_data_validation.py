def test_data_validation_profile(client, login):

    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "",
            "crp": "",
            "bio": "",
            "city": "marica",
            "template": "",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_data_response_profile(client, login):

    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "tutu",
            "crp": "05123457",
            "bio": "testando a bio",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["user_id"] is not None
    assert data["professional_name"] == "tutu"
    assert data["crp"] == "05123457"
    assert data["bio"] == "testando a bio"
    assert data["city"] == "marica"
    assert data["template"] == "template_01"


def test_slug_validation(client, login):

    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "ester vieira da vovó",
            "crp": "05123427",
            "bio": "testando a bio",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    data = response.json()
    assert data["slug"] == "ester-vieira-da-vovo-05123427"



def test_professional_name_min_length(client, profile_id, login):
    response = client.patch(
        f"api/v1/profile/{profile_id}",
        json={
            "professional_name": "ga",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_crp_min_length(client, profile_id, login):
    response = client.patch(
        f"api/v1/profile/{profile_id}",
        json={"crp": "1542"},
        headers={"Authorization": f"Bearer {login}"},
    )
    assert response.status_code == 422


def test_bio_min_length(client, profile_id, login):
    response = client.patch(
        f"api/v1/profile/{profile_id}",
        json={"bio": "teste"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


def test_template_min_length(client, profile_id, login):
    response = client.patch(
        f"api/v1/profile/{profile_id}",
        json={"template": ""},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422
