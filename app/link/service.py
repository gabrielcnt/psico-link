from app.link.exception import (
    LinkTitleAlreadyExistsError,
    LinkUrlAlreadyExistsError,
)
from app.link.models import Link
from app.link.repository import LinkRepository
from app.link.schemas import LinkCreate, LinkUpdate
from app.profile.models import Profile


class LinkService:
    def __init__(self, repository: LinkRepository):
        self.repository = repository

    def create_link(self, data: LinkCreate, profile: Profile) -> Link:
        existing_link_title = self.repository.get_by_profile_and_title(
            profile.id, data.title
        )

        if existing_link_title is not None:
            raise LinkTitleAlreadyExistsError("title already exists")

        existing_link_url = self.repository.get_by_profile_and_url(
            profile.id, str(data.url)
        )

        if existing_link_url is not None:
            raise LinkUrlAlreadyExistsError("link already exists")

        max_position = self.repository.get_max_position_by_profile_id(profile.id)

        if max_position is not None:
            max_position += 1

        else:
            max_position = 1

        link = Link(
            title=data.title, url=str(data.url), position=max_position, profile=profile
        )

        self.repository.create_link(link)

        return link

    def update_link(self, data: LinkUpdate, link: Link, profile: Profile) -> Link:

        if data.title is not None:
            existing_title = self.repository.get_by_profile_and_title(
                profile.id, data.title, link.id
            )

            if existing_title:
                raise LinkTitleAlreadyExistsError("title already exists")

            link.title = data.title

        if data.url is not None:
            existing_url = self.repository.get_by_profile_and_url(
                profile.id, str(data.url), link.id
            )

            if existing_url:
                raise LinkUrlAlreadyExistsError("url already exists")

            link.url = str(data.url)

        if data.position is not None:
            link.position = data.position

        self.repository.update_link(link)

        return link

    def delete_link(self, link: Link) -> None:
        self.repository.delete_link(link)
