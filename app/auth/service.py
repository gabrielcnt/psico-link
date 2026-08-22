from app.auth.models import User
from app.auth.repository import UserRepository
from app.auth.schemas import UserCreate
from app.shared.exceptions.handlers import EmailAlreadyExistError
from app.shared.security.password import hash_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(data.email)
        if existing_user:
            raise EmailAlreadyExistError("Email already registered")

        user = User(
            name=data.name, email=data.email, password_hash=hash_password(data.password)
        )

        return self.repository.create(user)
