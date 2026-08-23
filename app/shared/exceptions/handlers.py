from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.exceptions import EmailAlreadyExistError, InvalidCredentialError


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(EmailAlreadyExistError)
    async def email_already_exists_handler(
        request: Request, exc: EmailAlreadyExistError
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(InvalidCredentialError)
    async def invalid_credential_error(
        request: Request, exc: InvalidCredentialError
    ) -> None:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
