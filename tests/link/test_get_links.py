from app.link.repository import LinkRepository
from tests.test_database import TestSessionLocal


def test_list_profile_without_links(client, login, profile_id):
    response = client.get(
        f"/api/v1/profile/{profile_id}/links/",
        headers={"Authorization": f"Bearer {login}"},
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == []


def test_list_links_from_successful_profile(
    client, login, profile_id, link, second_link, third_link
):
    response = client.get(
        f"/api/v1/profile/{profile_id}/links/",
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["title"] == "tiktok"
    assert data[1]["title"] == "facebook"
    assert data[2]["title"] == "instagram"

    assert data[0]["position"] == 1
    assert data[1]["position"] == 2
    assert data[2]["position"] == 3


def test_list_links_belongs_another_profile(client, login, second_profile_id):
    response = client.get(
        f"/api/v1/profile/{second_profile_id}/links/",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_not_exists_profile(client, login):
    response = client.get(
        "/api/v1/profile/8a5ca3e8-d534-4087-bbc0-d9cba069ed8e/links/",
        headers={"Authorization": f"Bearer {login}"},
    )

    assert response.status_code == 404


def test_user_unauthenticated(client, profile_id):
    response = client.get(f"/api/v1/profile/{profile_id}/links/")

    assert response.status_code == 401


def test_list_position_links(client, login, profile_id, link, second_link, third_link):
    with TestSessionLocal() as session:
        repository = LinkRepository(session)
        # tiktok
        get_link_tiktok = repository.get_by_id(link["id"])
        get_link_tiktok.position = 2
        update_link_tiktok = repository.update_link(get_link_tiktok)
        tiktok = update_link_tiktok.position

        # facebook
        get_link_facebook = repository.get_by_id(second_link["id"])
        get_link_facebook.position = 3
        update_link_facebook = repository.update_link(get_link_facebook)
        facebook = update_link_facebook.position

        # instagram
        get_link_instagram = repository.get_by_id(third_link["id"])
        get_link_instagram.position = 1
        update_link_instagram = repository.update_link(get_link_instagram)
        instagram = update_link_instagram.position

    response = client.get(
        f"/api/v1/profile/{profile_id}/links",
        headers={"Authorization": f"Bearer {login}"},
    )
    data = response.json()
    assert data[0]["position"] == instagram
    assert data[1]["position"] == tiktok
    assert data[2]["position"] == facebook
