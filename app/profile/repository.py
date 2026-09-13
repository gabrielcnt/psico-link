from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.profile.models import Profile


class ProfileRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, profile: Profile) -> Profile:

        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)

        return profile

    def update(self, profile: Profile) -> Profile:

        self.session.commit()
        self.session.refresh(profile)

        return profile

    def get_by_id(self, profile_id: UUID) -> Profile | None:
        statement = select(Profile).where(Profile.id == profile_id)
        return self.session.scalar(statement)

    def get_by_user_id(self, user_id: UUID) -> Profile | None:
        statement = select(Profile).where(Profile.user_id == user_id)
        return self.session.scalar(statement)

    def get_by_profile_id(self, profile_id: UUID) -> Profile | None:
        statement = select(Profile).where(Profile.id == profile_id)
        return self.session.scalar(statement)

    def get_by_slug(self, slug: str) -> Profile | None:
        statement = select(Profile).where(Profile.slug == slug)
        return self.session.scalar(statement)
