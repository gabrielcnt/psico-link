from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.link.models import Link


class LinkRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_link(self, link: Link) -> Link:
        self.session.add(link)
        self.session.commit()
        self.session.refresh(link)
        return link

    def get_by_id(self, link_id: UUID) -> Link | None:
        statement = select(Link).where(Link.id == link_id)
        return self.session.scalar(statement)

    def get_by_profile_id(self, profile_id: UUID) -> list[Link]:
        statement = (
            select(Link).where(Link.profile_id == profile_id).order_by(Link.position)
        )
        return self.session.scalars(statement).all()

    def get_by_profile_and_title(
        self, profile_id: UUID, title: str, exclude_link_id: UUID | None = None
    ) -> Link | None:
        statement = select(Link).where(
            Link.profile_id == profile_id, Link.title == title
        )

        if exclude_link_id is not None:
            statement = statement.where(Link.id != exclude_link_id)
        return self.session.scalar(statement)

    def get_by_profile_and_url(
        self, profile_id: UUID, url: str, exclude_link_id: UUID | None = None
    ) -> Link | None:
        statement = select(Link).where(Link.profile_id == profile_id, Link.url == url)

        if exclude_link_id is not None:
            statement = statement.where(Link.id != exclude_link_id)
        return self.session.scalar(statement)

    def get_max_position_by_profile_id(self, profile_Id: UUID) -> Link | None:
        statement = select(func.max(Link.position)).where(
            Link.profile_id == profile_Id,
        )
        return self.session.scalar(statement)

    def update_link(self, link: Link) -> Link:
        self.session.commit()
        self.session.refresh(link)
        return link

    def delete_link(self, link: Link) -> None:
        self.session.delete(link)
        self.session.commit()
