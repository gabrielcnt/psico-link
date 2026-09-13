from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.link.exception import LinkNotFoundError
from app.link.models import Link
from app.link.repository import LinkRepository
from app.link.service import LinkService
from app.profile.dependencies import get_current_profile
from app.profile.models import Profile
from app.shared.database.dependencies import get_db


def get_link_service(session: Session = Depends(get_db)) -> LinkService:
    repository = LinkRepository(session)
    return LinkService(repository)


def get_current_link(
    link_id: UUID,
    session: Session = Depends(get_db),
    profile: Profile = Depends(get_current_profile),
) -> Link:

    repository = LinkRepository(session)

    link = repository.get_by_id(link_id)

    if link is None:
        raise LinkNotFoundError("link not found")

    if link.profile_id != profile.id:
        raise LinkNotFoundError("link not found")
    return link
