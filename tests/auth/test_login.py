def test_login_user(client):
    # criando usuario
    client.post(
        "api/v1/auth/register",
        json={
            "name": "Gabriel",
            "email": "gabriel@email.com",
            "password": "12345678",
        },
    )
    # fazer login
    response = client.post(
        "api/v1/auth/login",
        json={
            "email": "gabriel@email.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0

def test_login_invalid_email(client):
    # faz o login
    response = client.post(
        "api/v1/auth/login",
        json={
            "email": "sem_email@email.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 401

def test_login_invalid_password(client):
    # criando conta
    client.post(
        "api/v1/auth/register",
        json={
            "name": "Gumercindo",
            "email": "gugu@email.com",
            "password": "12345678",
        },
    )

    # fazendo login

    response = client.post(
        "api/v1/auth/login",
        json={
            "email": "gugu@email.com",
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401