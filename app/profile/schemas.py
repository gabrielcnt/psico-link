from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProfileCreate(BaseModel):
    professional_name: str = Field(min_length=3)
    crp: str = Field(min_length=8)
    bio: str = Field(min_length=10)
    city: str | None = None
    photo_url: str | None = None
    template: str = Field(min_length=1)


class ProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    professional_name: str
    crp: str
    bio: str
    city: str | None = None
    photo_url: str | None = None
    slug: str
    template: str

    model_config = ConfigDict(from_attributes=True)
