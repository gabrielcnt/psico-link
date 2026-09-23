from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.routes import get_current_user
from app.link.repository import LinkRepository
from app.profile.exceptions import ProfileNotFoundError
from app.profile.models import Profile
from app.profile.repository import ProfileRepository
from app.profile.service import ProfileService
from app.shared.database.dependencies import get_db
from app.specialty.repository import ProfileSpecialtyRepository, SpecialtyRepository


def get_current_profile(
    profile_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Profile:
    repository = ProfileRepository(session)

    profile = repository.get_by_id(profile_id)

    if profile is None:
        raise ProfileNotFoundError("Profile not found")

    if profile.user_id != current_user.id:
        raise ProfileNotFoundError("Profile not found")

    return profile


def get_profile_service(session: Session = Depends(get_db)) -> ProfileService:
    profile_repository = ProfileRepository(session)
    link_repository = LinkRepository(session)
    profile_specialty_repository = ProfileSpecialtyRepository(session)
    specialty_repository = SpecialtyRepository(session)

    return ProfileService(
        profile_repository, link_repository, profile_specialty_repository, specialty_repository
    )
