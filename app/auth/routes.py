from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.repository import UserRepository
from app.auth.schemas import (
    PasswordResetConfirm,
    PasswordResetRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.auth.service import UserService
from app.shared.database.dependencies import get_db
from app.shared.security.jwt import create_access_token

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


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):

    user = service.authenticate(email=form_data.username, password=form_data.password)

    access_token = create_access_token(str(user.id))

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/forgot-password")
def forgot_password(
    data: PasswordResetRequest, service: UserService = Depends(get_user_service)
):
    token = service.request_password_reset(data)
    return {"message": "If the email exists, a password reset link has been sent."}


@router.post("/reset-password")
def reset_password(
    data: PasswordResetConfirm, service: UserService = Depends(get_user_service)
):
    service.reset_password(data)
    return {"message": "Password reset successfully"}
