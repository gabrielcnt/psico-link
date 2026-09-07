from uuid import UUID

from app.auth.models import User
from app.profile.exceptions import (
    ProfileAlreadyExistsError,
    ProfileNotFoundError,
    ProfileUserUnauthorizedError,
    SlugAlreadyExistsError,
)
from app.profile.models import Profile
from app.profile.repository import ProfileRepository
from app.profile.schemas import ProfileCreate, ProfileUpdate
from app.shared.utils.slug import crp_treatment_to_slug, slug_treatment


class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

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

        self. repository.update(existing_profile)
        return existing_profile
