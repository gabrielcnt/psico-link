from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.link.schemas import LinkResponse
from app.specialty.schemas import PublicSpecialtyResponse


class ProfileCreate(BaseModel):
    professional_name: str = Field(min_length=3)
    crp: str = Field(min_length=8)
    bio: str = Field(min_length=10)
    city: str | None = None
    photo_url: HttpUrl | None = None
    template: str = Field(min_length=1)


class ProfileUpdate(BaseModel):
    professional_name: str | None = Field(default=None, min_length=3)
    crp: str | None = Field(default=None, min_length=8)
    bio: str | None = Field(default=None, min_length=10)
    city: str | None = None
    photo_url: HttpUrl | None = None
    template: str | None = Field(default=None, min_length=1)

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class ProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    professional_name: str
    crp: str
    bio: str
    city: str | None = None
    photo_url: HttpUrl | None = None
    slug: str
    template: str

    model_config = ConfigDict(from_attributes=True)


class PublicProfileResponse(BaseModel):
    professional_name: str
    photo_url: HttpUrl | None = None
    crp: str
    bio: str
    city: str | None = None
    specialties: list[PublicSpecialtyResponse]
    links: list[LinkResponse]

    model_config = ConfigDict(from_attributes=True)
