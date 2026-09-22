from fastapi import APIRouter, Depends

from app.profile.dependencies import get_current_profile
from app.profile.models import Profile
from app.specialty.dependencies import (
    get_current_profile_specialty,
    get_profile_specialty_service,
    get_specialty_service,
)
from app.specialty.models import ProfileSpecialty
from app.specialty.schemas import (
    ProfileSpecialtyCreate,
    ProfileSpecialtyResponse,
    ProfileSpecialtyUpdate,
    SpecialtyResponse,
)
from app.specialty.service import ProfileSpecialtyService, SpecialtyService

router = APIRouter(prefix="/profile", tags=["specialty"])


@router.post(
    "/{profile_id}/specialties/",
    response_model=ProfileSpecialtyResponse,
    status_code=201,
)
def create(
    data: ProfileSpecialtyCreate,
    profile: Profile = Depends(get_current_profile),
    service: ProfileSpecialtyService = Depends(get_profile_specialty_service),
) -> ProfileSpecialtyResponse:
    return service.create(data, profile)


@router.patch(
    "/{profile_id}/specialties/{specialty_id}",
    response_model=ProfileSpecialtyResponse,
    status_code=200,
)
def update(
    data: ProfileSpecialtyUpdate,
    profile_specialty: ProfileSpecialty = Depends(get_current_profile_specialty),
    service: ProfileSpecialtyService = Depends(get_profile_specialty_service),
) -> ProfileSpecialtyResponse:
    return service.update(data, profile_specialty)


@router.delete("/{profile_id}/specialties/{specialty_id}", status_code=204)
def delete(
    profile_specialty: ProfileSpecialty = Depends(get_current_profile_specialty),
    service: ProfileSpecialtyService = Depends(get_profile_specialty_service),
) -> None:
    return service.delete(profile_specialty)


@router.get(
    "/{profile_id}/specialties/",
    response_model=list[ProfileSpecialtyResponse],
    status_code=200,
)
def show_profile_specialties(
    profile: Profile = Depends(get_current_profile),
    service: ProfileSpecialtyService = Depends(get_profile_specialty_service),
) -> ProfileSpecialtyResponse:
    return service.get_by_profile(profile.id)


@router.get("/specialties", response_model=list[SpecialtyResponse], status_code=200)
def show_specialties(
    service: SpecialtyService = Depends(get_specialty_service),
) -> list[SpecialtyResponse]:
    return service.list_specialties()
