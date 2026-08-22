from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.shared.exceptions.handlers import register_exception_handlers

app = FastAPI(title="PsicoLink API", version="1.0.0")

app.include_router(auth_router, prefix="/api/v1")

register_exception_handlers(app)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
