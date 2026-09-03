import hashlib
import secrets


def generate_reset_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)

    return token, hash_reset_token(token)


def hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
