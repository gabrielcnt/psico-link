def test_successful_update(client, profile_id, login):
    response = client.patch(
        f"api/v1/profile/{profile_id}",
        json={"bio": "Uma nova descrição para o meu perfil"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200
    assert response.json()["bio"] == "Uma nova descrição para o meu perfil"
    assert response.json()["professional_name"] == "gabriel vieira"


def test_multiple_fields(client, profile_id, login):
    response = client.patch(
        f"api/v1/profile/{profile_id}",
        json={
            "professional_name": "Ivone Maria",
            "crp": "03/19786",
            "bio": "uma nova descrição de teste da bio",
            "city": "niteroi",
        },
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200
    assert response.json()["professional_name"] == "Ivone Maria"
    assert response.json()["bio"] == "uma nova descrição de teste da bio"
    assert response.json()["city"] == "niteroi"


def test_profile_not_found(client, login):
    response = client.patch(
        "api/v1/profile/00000000-0000-0000-0000-000000000001",
        json={"bio": "Uma nova descrição para testar se o profile será encontrado"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_user_changing_another_users_profile(client, login, profile_id):
    response = client.patch(
        f"api/v1/profile/{profile_id}",
        json={"bio": "Tentando mudar a descrição de outro usuario"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Unauthorized user"


def test_try_modify_slug(client, login, profile):

    response = client.patch(
        f"api/v1/profile/{profile['id']}",
        json={"slug": "tentativa-de-alterar-slug"},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 422


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


def test_update_profile_with_null_bio(client, profile_id, login):
    response = client.patch(
        f"api/v1/profile/{profile_id}",
        json={"bio": None},
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 200
    assert response.json()["bio"] == "cuidarei da sua loucura"
