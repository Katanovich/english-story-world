"""Pluggable file storage. Media metadata lives in PostgreSQL; binaries live here.

- `local`: files on disk under LOCAL_STORAGE_DIR (development / single server).
- `s3`:    not implemented yet — see S3Storage for the planned design.
"""

from functools import lru_cache
from pathlib import Path
from typing import BinaryIO, Protocol

from app.core.config import get_settings


class StorageError(Exception):
    pass


class Storage(Protocol):
    name: str

    def save(self, key: str, stream: BinaryIO, max_bytes: int) -> int:
        """Write the stream to `key`; return bytes written. Raise FileTooLarge over max_bytes."""
        ...

    def local_path(self, key: str) -> Path | None:
        """Filesystem path for direct serving, or None if the backend is remote."""
        ...

    def delete(self, key: str) -> None: ...


class FileTooLarge(StorageError):
    pass


class LocalStorage:
    name = "local"
    _CHUNK = 1024 * 1024

    def __init__(self, root: str) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        path = (self.root / key).resolve()
        # Keys are generated server-side, but guard against traversal anyway.
        if self.root not in path.parents:
            raise StorageError("Invalid storage key.")
        return path

    def save(self, key: str, stream: BinaryIO, max_bytes: int) -> int:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".part")
        written = 0
        try:
            with tmp.open("wb") as out:
                while chunk := stream.read(self._CHUNK):
                    written += len(chunk)
                    if written > max_bytes:
                        raise FileTooLarge()
                    out.write(chunk)
            tmp.replace(path)
        finally:
            tmp.unlink(missing_ok=True)
        return written

    def local_path(self, key: str) -> Path | None:
        path = self._path(key)
        return path if path.is_file() else None

    def delete(self, key: str) -> None:
        self._path(key).unlink(missing_ok=True)


class S3Storage:
    """Planned production backend (not implemented — no bucket is configured).

    Design: private bucket; the API issues short-lived presigned PUT URLs for direct
    browser uploads (admin only), records metadata with status PENDING, and marks the
    asset READY after a completion call verifies size/type with a HEAD request.
    Playback uses short-lived presigned GET URLs issued after the same authorization
    checks as `GET /media/{id}`. Credentials stay on the server.
    """

    name = "s3"

    def __init__(self) -> None:
        raise StorageError("STORAGE_BACKEND=s3 is not implemented yet. Use 'local'.")


@lru_cache
def get_storage() -> Storage:
    settings = get_settings()
    if settings.storage_backend == "local":
        return LocalStorage(settings.local_storage_dir)
    if settings.storage_backend == "s3":
        return S3Storage()
    raise StorageError(f"Unknown STORAGE_BACKEND '{settings.storage_backend}'.")
