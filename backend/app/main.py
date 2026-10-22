import logging

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.routes import admin_content, admin_progress, admin_users, auth, learning, media
from app.core.config import get_settings
from app.core.errors import install_error_handlers
from app.core.middleware import OriginCheckMiddleware, RequestLogMiddleware
from app.db.session import engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="English Story World API",
        version="0.1.0",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url="/docs",
        redoc_url=None,
    )
    install_error_handlers(app)
    app.add_middleware(OriginCheckMiddleware, allowed_origins=settings.cors_origins)
    app.add_middleware(RequestLogMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Content-Type"],
    )

    api = APIRouter(prefix=settings.api_prefix)

    @api.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}

    api.include_router(auth.router)
    api.include_router(admin_users.router)
    api.include_router(admin_progress.router)
    api.include_router(admin_content.router)
    api.include_router(learning.router)
    api.include_router(learning.me)
    api.include_router(media.router)
    api.include_router(media.admin)
    app.include_router(api)
    return app


app = create_app()
