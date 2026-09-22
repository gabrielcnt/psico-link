import uuid

from sqlalchemy import ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base


class Specialty(Base):
    __tablename__ = "specialties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    profile_specialties: Mapped[list["ProfileSpecialty"]] = relationship(
        back_populates="specialty", cascade="all, delete-orphan"
    )


class ProfileSpecialty(Base):
    __tablename__ = "profile_specialties"

    __table_args__ = (PrimaryKeyConstraint("profile_id", "specialty_id"),)

    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False
    )
    specialty_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("specialties.id"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    profile: Mapped["Profile"] = relationship(back_populates="profile_specialties")

    specialty: Mapped["Specialty"] = relationship(back_populates="profile_specialties")
