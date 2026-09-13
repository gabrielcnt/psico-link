from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LinkCreate(BaseModel):
    title: str = Field(min_length=3)
    url: HttpUrl


class LinkUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3)
    url: HttpUrl | None = None
    position: int | None = None


class LinkResponse(BaseModel):
    id: UUID
    profile_id: UUID
    title: str
    url: HttpUrl
    position: int

    model_config = ConfigDict(from_attributes=True)
