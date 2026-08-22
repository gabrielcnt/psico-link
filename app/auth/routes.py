from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.repository import UserRepository
from app.auth.schemas import UserCreate, UserResponse
from app.auth.service import UserService
from app.shared.database.dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def get_user_service(
    session: Session = Depends(get_db),
) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(data)
