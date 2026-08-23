class EmailAlreadyExistError(Exception):
    """Raised when attempting to register an already registered email."""

class InvalidCredentialError(Exception):
    pass