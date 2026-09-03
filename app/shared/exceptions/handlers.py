from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.exceptions import EmailAlreadyExistError, InvalidCredentialError
from app.profile.exceptions import ProfileAlreadyExistsError, SlugAlreadyExistsError


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(EmailAlreadyExistError)
    async def email_already_exists_handler(
        request: Request, exc: EmailAlreadyExistError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(InvalidCredentialError)
    async def invalid_credential_error(
        request: Request, exc: InvalidCredentialError
    ) -> JSONResponse:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

    @app.exception_handler(ProfileAlreadyExistsError)
    async def profile_already_exist_error(
        request: Request, exc: ProfileAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(SlugAlreadyExistsError)
    async def slug_already_exists_error(
        request: Request, exc: SlugAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})
