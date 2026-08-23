from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: UUID) -> User | None:
        statement = select(User).where(User.id == id)

        return self.session.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self.session.scalar(statement)

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
