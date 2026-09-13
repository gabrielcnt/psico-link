from datetime import UTC, datetime, timedelta

from app.auth.exceptions import EmailAlreadyExistError, InvalidCredentialError
from app.auth.models import PasswordResetToken, User
from app.auth.password_reset import generate_reset_token, hash_reset_token
from app.auth.repository import UserRepository
from app.auth.schemas import PasswordResetConfirm, PasswordResetRequest, UserCreate
from app.shared.security.password import hash_password, verify_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(data.email)
        if existing_user:
            raise EmailAlreadyExistError("Email already registered")

        user = User(
            name=data.name, email=data.email, password_hash=hash_password(data.password)
        )

        return self.repository.create(user)

    def authenticate(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialError()

        return user

    def request_password_reset(self, data: PasswordResetRequest) -> str | None:
        user = self.repository.get_by_email(data.email)

        if user is None:
            return None

        token, token_hash = generate_reset_token()

        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(UTC) + timedelta(minutes=30),
        )

        self.repository.create_password_reset_token(reset_token)

        return token

    def validate_password_reset_token(self, token: str) -> PasswordResetToken:

        token_hash = hash_reset_token(token)

        reset_token = self.repository.get_password_reset_token(token_hash)

        if reset_token is None:
            raise InvalidCredentialError("Invalid reset token")

        if reset_token.used_at is not None:
            raise InvalidCredentialError("Reset token already used")

        if reset_token.expires_at <= datetime.now(UTC):
            raise InvalidCredentialError("Reset token expired")

        return reset_token

    def reset_password(self, data: PasswordResetConfirm) -> None:
        reset_token = self.validate_password_reset_token(data.token)

        user = self.repository.get_by_id(reset_token.user_id)

        if user is None:
            raise InvalidCredentialError("User not found")

        password_hash = hash_password(data.new_password)

        self.repository.update_password(user, password_hash)

        self.repository.mark_password_reset_token_as_used(reset_token)
