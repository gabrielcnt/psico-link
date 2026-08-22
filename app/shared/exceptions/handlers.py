from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.exceptions import EmailAlreadyExistError


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
