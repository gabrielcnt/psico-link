from uuid import UUID

from app.profile.models import Profile
from app.specialty.exceptions import (
    ProfileSpecialtyAlreadyExistsError,
    ProfileSpecialtyPositionNoneError,
    SpecialtyNotFoundError,
)
from app.specialty.models import ProfileSpecialty, Specialty
from app.specialty.repository import ProfileSpecialtyRepository, SpecialtyRepository
from app.specialty.schemas import ProfileSpecialtyCreate, ProfileSpecialtyUpdate


class SpecialtyService:
    def __init__(self, repository: SpecialtyRepository):
        self.repository = repository

    def list_specialties(self) -> list[Specialty]:
        return self.repository.list_specialties()


class ProfileSpecialtyService:
    def __init__(
        self,
        repository: ProfileSpecialtyRepository,
        specialty_repository: SpecialtyRepository,
    ):
        self.repository = repository
        self.specialty_repository = specialty_repository

    def create(
        self, data: ProfileSpecialtyCreate, profile: Profile
    ) -> ProfileSpecialty:
        specialty = self.specialty_repository.get_by_id(data.specialty_id)

        if specialty is None:
            raise SpecialtyNotFoundError("specialty not found")

        existing_profile_and_specialty = self.repository.get_by_profile_and_specialty(
            profile.id, data.specialty_id
        )

        if existing_profile_and_specialty is not None:
            raise ProfileSpecialtyAlreadyExistsError("Specialty exists")

        max_position = self.repository.get_by_max_position_profile_id(profile.id)

        if max_position is not None:
            max_position += 1

        else:
            max_position = 1

        profile_specialty = ProfileSpecialty(
            profile_id=profile.id, specialty_id=data.specialty_id, position=max_position
        )

        return self.repository.create(profile_specialty)

    def update(
        self,
        data: ProfileSpecialtyUpdate,
        profile_specialty: ProfileSpecialty,
    ) -> ProfileSpecialty:

        if data.position is None:
            raise ProfileSpecialtyPositionNoneError("The position cannot be empty.")

        profile_specialty.position = data.position

        return self.repository.update(profile_specialty)

    def delete(self, profile_specialty: ProfileSpecialty) -> None:
        self.repository.delete(profile_specialty)

    def get_by_profile(self, profile_id: UUID) -> list[ProfileSpecialty]:
        return self.repository.get_by_profile(profile_id)
