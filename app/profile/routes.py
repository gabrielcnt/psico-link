from uuid import UUID

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.profile.dependencies import get_profile_service
from app.profile.schemas import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
    PublicProfileResponse,
)
from app.profile.service import ProfileService

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", response_model=ProfileResponse, status_code=201)
def create_profile(
    data: ProfileCreate,
    service: ProfileService = Depends(get_profile_service),
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    return service.create_profile(data, current_user)


@router.patch("/{profile_id}", response_model=ProfileResponse, status_code=200)
def update_profile(
    profile_id: UUID,
    data: ProfileUpdate,
    service: ProfileService = Depends(get_profile_service),
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    return service.update_profile(profile_id, data, current_user)


@router.get("/{slug}", response_model=PublicProfileResponse, status_code=200)
def public_profile(
    slug: str, service: ProfileService = Depends(get_profile_service)
) -> PublicProfileResponse:
    return service.get_public_profile(slug)
