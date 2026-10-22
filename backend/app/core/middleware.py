import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger("app.request")

_UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class RequestLogMiddleware(BaseHTTPMiddleware):
    """Logs method, path, status and duration only — never bodies, cookies or query strings."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "%s %s -> %s (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response


def _origin_host(origin: str) -> str:
    return origin.split("://", 1)[-1].rstrip("/").lower()


class OriginCheckMiddleware(BaseHTTPMiddleware):
    """CSRF defence in depth (in addition to SameSite=Lax cookies): state-changing requests
    that carry an Origin header must come from an allowed frontend origin, or from the same
    host the request was sent to (e.g. a tunnel/public URL proxied through the frontend).
    Browsers do not let a foreign site forge the Host / X-Forwarded-Host headers."""

    def __init__(self, app, allowed_origins: list[str]) -> None:  # noqa: ANN001
        super().__init__(app)
        self.allowed = set(allowed_origins)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        origin = request.headers.get("origin")
        if request.method in _UNSAFE_METHODS and origin and not self._allowed(request, origin):
            return JSONResponse(
                status_code=403,
                content={"error": {"code": "forbidden", "message": "Origin not allowed."}},
            )
        return await call_next(request)

    def _allowed(self, request: Request, origin: str) -> bool:
        if origin in self.allowed:
            return True
        host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
        return _origin_host(origin) == host.split(",")[0].strip().lower()
