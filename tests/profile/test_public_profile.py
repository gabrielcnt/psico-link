def test_public_profile_success(
    client,
    profile_slug,
):
    response = client.get(f"/api/v1/profile/{profile_slug}")

    data = response.json()

    assert response.status_code == 200

    assert data["professional_name"] == "gabriel vieira"
    assert data["photo_url"] == None
    assert data["crp"] == "06/46872"
    assert data["bio"] == "cuidarei da sua loucura"
    assert data["city"] == "marica"


def test_return_specialties_profile(
    client,
    profile_slug,
    specialty_id,
):
    response = client.get(f"/api/v1/profile/{profile_slug}")

    data = response.json()

    assert isinstance(data["specialties"], list)
    assert len(data["specialties"]) == 1
    assert data["specialties"][0]["position"] == 1
    assert data["specialties"][0]["id"] == specialty_id
    assert data["specialties"][0]["name"] == "Psicologia clínica"


def test_return_link_profile(client, profile_slug, link):
    response = client.get(f"/api/v1/profile/{profile_slug}")

    data = response.json()
    print(data)
    assert isinstance(data["links"], list)
    assert len(data["links"]) == 1
    assert data["links"][0]["title"] == "tiktok"
    assert data["links"][0]["url"] == "https://www.tiktok.com/"
    assert data["links"][0]["position"] == 1


def test_slug_not_found(client):
    response = client.get("/api/v1/profile/maria-8798645")

    assert response.status_code == 404


def test_does_not_return_private_user_data(client, profile_slug, link, specialty_id):
    response = client.get(f"/api/v1/profile/{profile_slug}")
    data = response.json()
    assert "email" not in data
    assert "hashed_password" not in data
    assert "is_superuser" not in data
    assert "is_verified" not in data


def test_return_only_data_for_queried_profile(
    client,
    profile_slug,
    link,
    specialty_id,
    second_link,
):
    response = client.get(f"/api/v1/profile/{profile_slug}/")
    data = response.json()
    print(data)
    assert data["links"][0]["id"] == link["id"]
    assert data["specialties"][0]["id"] == specialty_id

    assert second_link not in [link["id"] for link in data["links"]]


def test_profile_without_links(client, profile_slug):
    response = client.get(f"/api/v1/profile/{profile_slug}")

    data = response.json()
    print(data)

    assert response.status_code == 200
    assert data["links"] == []


def test_profile_without_specialties(client, profile_slug):
    response = client.get(f"/api/v1/profile/{profile_slug}")

    data = response.json()

    assert response.status_code == 200
    assert data["specialties"] == []
