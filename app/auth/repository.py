from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.models import PasswordResetToken, User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: UUID) -> User | None:
        statement = select(User).where(User.id == id)

        return self.session.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self.session.scalar(statement)

    def create_password_reset_token(
        self, reset_token: PasswordResetToken
    ) -> PasswordResetToken:
        self.session.add(reset_token)
        self.session.commit()
        self.session.refresh(reset_token)

        return reset_token

    def get_password_reset_token(self, token_hash: str) -> PasswordResetToken | None:
        statement = select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash
        )

        return self.session.scalar(statement)

    def update_password(self, user: User, password_hash: str) -> User:
        user.password_hash = password_hash
        self.session.commit()
        self.session.refresh(user)

        return user

    def mark_password_reset_token_as_used(
        self, reset_token: PasswordResetToken
    ) -> PasswordResetToken:
        reset_token.used_at = datetime.now(UTC)

        self.session.commit()
        self.session.refresh(reset_token)

        return reset_token

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
