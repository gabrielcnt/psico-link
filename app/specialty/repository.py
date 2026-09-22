from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.specialty.models import ProfileSpecialty, Specialty


class SpecialtyRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, specialty_id: UUID) -> Specialty | None:
        statement = select(Specialty).where(Specialty.id == specialty_id)

        return self.session.scalar(statement)

    def list_specialties(self) -> list[Specialty]:
        statement = select(Specialty)
        return self.session.scalars(statement).all()


class ProfileSpecialtyRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, profile_specialty: ProfileSpecialty) -> ProfileSpecialty:
        self.session.add(profile_specialty)
        self.session.commit()
        self.session.refresh(profile_specialty)
        return profile_specialty

    def update(self, profile_specialty: ProfileSpecialty) -> ProfileSpecialty:
        self.session.commit()
        self.session.refresh(profile_specialty)
        return profile_specialty

    def delete(self, profile_specialty: ProfileSpecialty) -> None:
        self.session.delete(profile_specialty)
        self.session.commit()

    def get_by_profile_and_specialty(
        self, profile_id: UUID, specialty_id: UUID
    ) -> ProfileSpecialty | None:
        statement = select(ProfileSpecialty).where(
            ProfileSpecialty.profile_id == profile_id,
            ProfileSpecialty.specialty_id == specialty_id,
        )
        return self.session.scalar(statement)

    def get_by_profile(self, profile_id: UUID) -> list[ProfileSpecialty]:
        statement = (
            select(ProfileSpecialty)
            .where(ProfileSpecialty.profile_id == profile_id)
            .order_by(ProfileSpecialty.position)
        )
        return self.session.scalars(statement).all()

    def get_by_max_position_profile_id(self, profile_id: UUID) -> int | None:
        statement = select(func.max(ProfileSpecialty.position)).where(
            ProfileSpecialty.profile_id == profile_id
        )
        return self.session.scalar(statement)
