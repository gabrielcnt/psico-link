def test_list_all_specialties(client, specialties):
    response = client.get("/api/v1/profile/specialties")

    data = response.json()
    print(data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 15


def test_list_specialties_data(client, specialties):
    response = client.get("/api/v1/profile/specialties")

    data = response.json()

    fixture_ids = [str(specialty.id) for specialty in specialties]

    response_ids = [item["id"] for item in data]

    for item in data:
        assert "id" in item
        assert "name" in item
        assert item["id"]

    assert response_ids == fixture_ids

def test_allow_access_without_authentication(client, specialties):
    response = client.get("/api/v1/profile/specialties")

    assert response.status_code == 200