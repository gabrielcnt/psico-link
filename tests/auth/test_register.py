from uuid import uuid4


def test_register_user(client):
    email = f"{uuid4()}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Gabriel", "email": email, "password": "12345678"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Gabriel"
    assert data["email"] == email
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    email = f"{uuid4()}@example.com"

    response = client.post(
        "api/v1/auth/register",
        json={
            "name": "Gabriel",
            "email": email,
            "password": "12345678",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "api/v1/auth/register",
        json={
            "name": "Gabriel",
            "email": email,
            "password": "12345678",
        },
    )

    assert response.status_code == 409


def test_register_invalid_email(client):
    response = client.post(
        "api/v1/auth/register",
        json={
            "name": "Gabriel",
            "email": "gabriel234.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 422


def test_register_missing_name(client):
    response = client.post(
        "api/v1/auth/register",
        json={
            "email": "gabriel32@email.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 422
