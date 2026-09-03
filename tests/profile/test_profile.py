def test_create_profile_success(client, login):

    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "gabriel vieira",
            "crp": "06/46872",
            "bio": "cuidarei da sua loucura",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )
    print(response.status_code)
    print(response.json())

    assert response.status_code == 201


def test_user_already_profile(client, login):

    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "gabriel vieira",
            "crp": "06/46872",
            "bio": "cuidarei da sua loucura",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )
    assert response.status_code == 201

    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "gabriel vieira",
            "crp": "06/46872",
            "bio": "cuidarei da sua loucura",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )
    assert response.status_code == 409


def test_user_create_existing_profile(client, login):

    response = client.post(
        "api/v1/profile",
        json={
            "professional_name": "gabriel vieira",
            "crp": "06/46872",
            "bio": "cuidarei da sua loucura",
            "city": "marica",
            "template": "template_01",
        },
        headers={"Authorization": f"Bearer {login}"},
    )
    assert response.status_code == 201

    response = client.post(
            "api/v1/profile",
            json={
                "professional_name": "gabriel vieira",
                "crp": "06/46872",
                "bio": "cuidarei da sua loucura",
                "city": "marica",
                "template": "template_01",
            },
            headers={"Authorization": f"Bearer {login}"},
        )
    assert response.status_code == 409
