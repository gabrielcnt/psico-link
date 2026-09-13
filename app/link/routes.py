from fastapi import APIRouter, Depends

from app.link.dependencies import get_current_link, get_link_service
from app.link.models import Link
from app.link.schemas import LinkCreate, LinkResponse, LinkUpdate
from app.link.service import LinkService
from app.profile.dependencies import get_current_profile
from app.profile.models import Profile

router = APIRouter(prefix="/profile", tags=["links"])


@router.post("/{profile_id}/links", response_model=LinkResponse, status_code=201)
def create_link(
    data: LinkCreate,
    profile: Profile = Depends(get_current_profile),
    service: LinkService = Depends(get_link_service),
) -> LinkResponse:
    return service.create_link(data, profile)


@router.patch(
    "/{profile_id}/links/{link_id}/", response_model=LinkResponse, status_code=200
)
def update_link(
    data: LinkUpdate,
    profile: Profile = Depends(get_current_profile),
    link: Link = Depends(get_current_link),
    service: LinkService = Depends(get_link_service),
) -> LinkResponse:
    return service.update_link(data, link, profile)


@router.delete("/{profile_id}/links/{link_id}/", status_code=204)
def delete_link(
    link: Link = Depends(get_current_link),
    service: LinkService = Depends(get_link_service),
):
    service.delete_link(link)
