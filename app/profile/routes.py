from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.profile.repository import ProfileRepository
from app.profile.schemas import ProfileCreate, ProfileResponse
from app.profile.service import ProfileService
from app.shared.database.dependencies import get_db

router = APIRouter(prefix="/profile", tags=["Profile"])


def get_profile_service(session: Session = Depends(get_db)) -> ProfileService:
    repository = ProfileRepository(session)

    return ProfileService(repository)


@router.post("/", response_model=ProfileResponse, status_code=201)
def create_profile(
    data: ProfileCreate,
    service: ProfileService = Depends(get_profile_service),
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    return service.create_profile(data, current_user)
