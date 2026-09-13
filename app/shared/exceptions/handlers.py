from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.exceptions import EmailAlreadyExistError, InvalidCredentialError
from app.link.exception import (
    LinkNotFoundError,
    LinkTitleAlreadyExistsError,
    LinkUrlAlreadyExistsError,
)
from app.profile.exceptions import (
    ProfileAlreadyExistsError,
    ProfileNotFoundError,
    ProfileUserUnauthorizedError,
    SlugAlreadyExistsError,
)


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

    @app.exception_handler(ProfileNotFoundError)
    async def profile_not_found_error(
        request: Request, exc: ProfileNotFoundError
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ProfileUserUnauthorizedError)
    async def profile_user_unauthorized_error(
        request: Request, exc: ProfileUserUnauthorizedError
    ) -> JSONResponse:
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(LinkTitleAlreadyExistsError)
    async def link_title_already_exists_error(
        request: Request, exc: LinkTitleAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(LinkUrlAlreadyExistsError)
    async def link_url_already_exists_error(
        request: Request, exc: LinkUrlAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(LinkNotFoundError)
    async def link_not_found_error(
        request: Request, exc: LinkNotFoundError
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})
