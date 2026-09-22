from sqlalchemy import select
from sqlalchemy.orm import Session

from app.specialty.models import Specialty

SPECIALITIES = [
    "Psicologia Clínica",
    "Psicologia Infantil",
    "Psicologia do Adolescente",
    "Psicologia de Adultos",
    "Psicologia de Casal",
    "Psicologia Familiar",
    "Psicologia Hospitalar",
    "Psicologia Organizacional",
    "Psicologia do Esporte",
    "Psicologia Escolar",
    "Psicologia Social",
    "Psicologia Jurídica",
    "Psicologia do Trânsito",
    "Psicologia Neuropsicológica",
    "Psicologia da Saúde",
]


def seed_specialties(session: Session) -> None:
    for specialty in SPECIALITIES:
        statement = select(Specialty).where(Specialty.name == specialty)
        result = session.scalar(statement)

        if result:
            continue

        session.add(Specialty(name=specialty))

    session.commit()


if __name__ == "__main__":
    seed_specialties()
