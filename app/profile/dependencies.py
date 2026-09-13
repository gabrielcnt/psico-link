from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.routes import get_current_user
from app.profile.exceptions import ProfileNotFoundError
from app.profile.models import Profile
from app.profile.repository import ProfileRepository
from app.shared.database.dependencies import get_db


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
