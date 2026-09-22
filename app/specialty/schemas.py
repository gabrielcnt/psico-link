from uuid import UUID

from pydantic import BaseModel, Field


class SpecialtyCreate(BaseModel):
    name: str = Field(min_length=3)


class SpecialtyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3)


class SpecialtyResponse(BaseModel):
    id: UUID
    name: str


class ProfileSpecialtyCreate(BaseModel):
    specialty_id: UUID


class ProfileSpecialtyUpdate(BaseModel):
    position: int | None = None


class ProfileSpecialtyResponse(BaseModel):
    profile_id: UUID
    specialty_id: UUID
    position: int
