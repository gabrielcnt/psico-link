from app.auth.password_reset import generate_reset_token, hash_reset_token


def test_request_password_reset(client, monkeypatch):

    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Gabriel",
            "email": "gabriel@email.com",
            "password": "12345678",
        },
    )

    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": "gabriel@email.com",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "If the email exists, a password reset link has been sent."
    )


def test_generate_reset_token():
    token, token_hah = generate_reset_token()

    assert token
    assert token_hah
    assert token != token_hah


def test_reset_password(client, monkeypatch):
    token = "token-de-teste"

    def fake_generate_reset_token():
        return token, hash_reset_token(token)

    monkeypatch.setattr(
        "app.auth.service.generate_reset_token", fake_generate_reset_token
    )

    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Gabriel",
            "email": "gabriel@email.com",
            "password": "12345678",
        },
    )

    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": "gabriel@email.com",
        },
    )

    print(response.json())
    
    assert response.status_code == 200

    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": token,
            "new_password": "87654321",
        },
    )
    print(response.json())
    assert response.status_code == 200

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "gabriel@email.com", "password": "87654321"},
    )

    assert response.status_code == 200
