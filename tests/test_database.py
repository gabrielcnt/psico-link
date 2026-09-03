from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.shared.config.settings import settings

test_engine = create_engine(settings.test_database_url)

TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()
