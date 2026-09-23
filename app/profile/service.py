from uuid import UUID

from app.auth.models import User
from app.link.repository import LinkRepository
from app.profile.exceptions import (
    ProfileAlreadyExistsError,
    ProfileNotFoundError,
    ProfileUserUnauthorizedError,
    SlugAlreadyExistsError,
)
from app.profile.models import Profile
from app.profile.repository import ProfileRepository
from app.profile.schemas import ProfileCreate, ProfileUpdate, PublicProfileResponse
from app.shared.utils.slug import crp_treatment_to_slug, slug_treatment
from app.specialty.repository import ProfileSpecialtyRepository, SpecialtyRepository
from app.specialty.schemas import PublicSpecialtyResponse


class ProfileService:
    def __init__(
        self,
        repository: ProfileRepository,
        link_repository: LinkRepository,
        profile_specialty_repository: ProfileSpecialtyRepository,
        specialty_repository: SpecialtyRepository,
    ):
        self.repository = repository
        self.link_repository = link_repository
        self.profile_specialty_repository = profile_specialty_repository
        self.specialty_repository = specialty_repository

    def create_profile(self, data: ProfileCreate, user: User) -> Profile:
        existing_profile = self.repository.get_by_user_id(user.id)

        if existing_profile is not None:
            raise ProfileAlreadyExistsError("Profile already exists")

        name = slug_treatment(data.professional_name)
        crp = crp_treatment_to_slug(data.crp)
        slug = f"{name}-{crp}"

        exisating_slug = self.repository.get_by_slug(slug)

        if exisating_slug is not None:
            raise SlugAlreadyExistsError("Slug already exists")

        profile = Profile(
            user_id=user.id,
            professional_name=data.professional_name,
            crp=data.crp,
            bio=data.bio,
            slug=slug,
            city=data.city,
            photo_url=data.photo_url,
            template=data.template,
        )

        self.repository.create(profile)

        return profile

    def update_profile(
        self, profile_id: UUID, data: ProfileUpdate, user: User
    ) -> Profile:
        existing_profile = self.repository.get_by_profile_id(profile_id)

        if existing_profile is None:
            raise ProfileNotFoundError("Profile not found")

        if existing_profile.user_id != user.id:
            raise ProfileUserUnauthorizedError("Unauthorized user")

        update_data = data.model_dump(exclude_none=True)

        for k, i in update_data.items():
            setattr(existing_profile, k, i)

        self.repository.update(existing_profile)
        return existing_profile

    def get_public_profile(self, slug: str) -> PublicProfileResponse:
        existing_slug = self.repository.get_by_slug(slug)

        if existing_slug is None:
            raise ProfileNotFoundError("Profile not found")

        links = self.link_repository.get_by_profile_id(existing_slug.id)
        specialties = self.profile_specialty_repository.get_by_profile(existing_slug.id)

        public_specialties = []

        for profile_specialty in specialties:
            specialty_id = profile_specialty.specialty_id
            specialty = self.specialty_repository.get_by_id(specialty_id)
            position = profile_specialty.position

            specialty_response = PublicSpecialtyResponse(
                id=specialty_id, name=specialty.name, position=position
            )

            public_specialties.append(specialty_response)

        public_profile = PublicProfileResponse(
            professional_name=existing_slug.professional_name,
            photo_url=existing_slug.photo_url,
            crp=existing_slug.crp,
            bio=existing_slug.bio,
            city=existing_slug.city,
            specialties=public_specialties,
            links=links,
        )

        return public_profile
