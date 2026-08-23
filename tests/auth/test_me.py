import jwt

from app.shared.config.settings import settings


def test_get_current_user(client):
    register_response = client.post(
        "api/v1/auth/register",
        json={
            "name": "tchuco",
            "email": "tchuco@email.com",
            "password": "12345678",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "api/v1/auth/login",
        json={
            "email": "tchuco@email.com",
            "password": "12345678",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "tchuco@email.com"
    assert data["name"] == "tchuco"


def test_get_current_user_without_token(client):
    response = client.get("api/v1/auth/me")

    assert response.status_code == 401


def test_get_current_user_with_invalid_token(client):
    response = client.get(
        "api/v1/auth/me",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401


def test_get_current_user_with_expired_token(client):
    token = jwt.encode(
        {
            "sub": "00000000-0000-0000-0000-000000000000",
            "exp": 0,
        },
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    response = client.get(
        "api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
