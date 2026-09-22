from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.profile.dependencies import get_current_profile
from app.profile.models import Profile
from app.shared.database.dependencies import get_db
from app.specialty.exceptions import ProfileSpecialtyNotFoundError
from app.specialty.models import ProfileSpecialty
from app.specialty.repository import ProfileSpecialtyRepository, SpecialtyRepository
from app.specialty.service import ProfileSpecialtyService, SpecialtyService


def get_profile_specialty_service(
    session: Session = Depends(get_db),
) -> ProfileSpecialtyService:
    repository = ProfileSpecialtyRepository(session)
    specialty_repository = SpecialtyRepository(session)
    return ProfileSpecialtyService(repository, specialty_repository)


def get_specialty_service(session: Session = Depends(get_db)) -> SpecialtyService:
    repository = SpecialtyRepository(session)
    return SpecialtyService(repository)


def get_current_profile_specialty(
    specialty_id: UUID,
    profile: Profile = Depends(get_current_profile),
    session: Session = Depends(get_db),
) -> ProfileSpecialty:
    repository = ProfileSpecialtyRepository(session)

    profile_specialty = repository.get_by_profile_and_specialty(
        profile.id, specialty_id
    )

    if profile_specialty is None:
        raise ProfileSpecialtyNotFoundError("profile specialty not found")

    return profile_specialty
