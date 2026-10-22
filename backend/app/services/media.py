"""Upload validation and storage of media assets."""

import uuid
from dataclasses import dataclass
from pathlib import PurePath
from typing import BinaryIO

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import AppError
from app.models import MediaAsset, User
from app.models.enums import MediaStatus, MediaType, UserRole
from app.storage import FileTooLarge, get_storage


@dataclass(frozen=True)
class Format:
    mime: str
    media_type: MediaType
    extensions: tuple[str, ...]


# Allow-list. SVG is deliberately excluded (it can carry scripts).
FORMATS = [
    Format("image/png", MediaType.IMAGE, (".png",)),
    Format("image/jpeg", MediaType.IMAGE, (".jpg", ".jpeg")),
    Format("image/webp", MediaType.IMAGE, (".webp",)),
    Format("audio/mpeg", MediaType.AUDIO, (".mp3",)),
    Format("audio/wav", MediaType.AUDIO, (".wav",)),
    Format("audio/ogg", MediaType.AUDIO, (".ogg", ".oga")),
    Format("audio/webm", MediaType.AUDIO, (".webm", ".weba")),
    Format("audio/mp4", MediaType.AUDIO, (".m4a",)),
    Format("video/mp4", MediaType.VIDEO, (".mp4", ".m4v")),
    Format("video/webm", MediaType.VIDEO, (".webm",)),
    Format("text/vtt", MediaType.SUBTITLE, (".vtt",)),
]


def _sniff(head: bytes) -> set[str]:
    """MIME types consistent with the file's first bytes (magic numbers)."""
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return {"image/png"}
    if head.startswith(b"\xff\xd8\xff"):
        return {"image/jpeg"}
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return {"image/webp"}
    if head[:4] == b"RIFF" and head[8:12] == b"WAVE":
        return {"audio/wav"}
    if head.startswith(b"ID3") or (len(head) > 1 and head[0] == 0xFF and head[1] & 0xE0 == 0xE0):
        return {"audio/mpeg"}
    if head.startswith(b"OggS"):
        return {"audio/ogg"}
    if head.startswith(b"\x1a\x45\xdf\xa3"):
        return {"audio/webm", "video/webm"}
    if head[4:8] == b"ftyp":
        return {"video/mp4", "audio/mp4"}
    if head.lstrip(b"\xef\xbb\xbf").startswith(b"WEBVTT"):
        return {"text/vtt"}
    return set()


def _limit_bytes(media_type: MediaType) -> int:
    s = get_settings()
    mb = {
        MediaType.IMAGE: s.max_image_mb,
        MediaType.AUDIO: s.max_audio_mb,
        MediaType.VIDEO: s.max_video_mb,
        MediaType.SUBTITLE: 1,
    }[media_type]
    return mb * 1024 * 1024


def detect_format(filename: str, stream: BinaryIO, expected: MediaType) -> Format:
    ext = PurePath(filename).suffix.lower()
    head = stream.read(64)
    stream.seek(0)
    sniffed = _sniff(head)
    for fmt in FORMATS:
        if fmt.media_type == expected and ext in fmt.extensions and fmt.mime in sniffed:
            return fmt
    allowed = sorted({e for f in FORMATS if f.media_type == expected for e in f.extensions})
    raise AppError(
        415,
        f"Unsupported or mismatched file. Allowed {expected.value.lower()} types: "
        + ", ".join(allowed),
    )


def store_upload(
    db: Session,
    *,
    uploader: User,
    filename: str,
    stream: BinaryIO,
    media_type: MediaType,
    alt_text: str | None = None,
    transcript: str | None = None,
) -> MediaAsset:
    safe_name = PurePath(filename or "upload").name[:255]
    fmt = detect_format(safe_name, stream, media_type)
    storage = get_storage()
    asset_id = uuid.uuid4()
    # Server-generated key: never derived from user input.
    key = f"{media_type.value.lower()}/{asset_id.hex[:2]}/{asset_id.hex}{fmt.extensions[0]}"
    limit = _limit_bytes(media_type)
    try:
        size = storage.save(key, stream, limit)
    except FileTooLarge as exc:
        raise AppError(413, f"File is too large (max {limit // (1024 * 1024)} MB).") from exc
    asset = MediaAsset(
        id=asset_id,
        media_type=media_type,
        storage_backend=storage.name,
        storage_key=key,
        original_filename=safe_name,
        mime_type=fmt.mime,
        size_bytes=size,
        status=MediaStatus.READY,
        alt_text=alt_text,
        transcript=transcript,
        uploaded_by_id=uploader.id,
    )
    db.add(asset)
    db.flush()
    return asset


def is_private_recording(db: Session, asset: MediaAsset) -> bool:
    """Media uploaded by a student (voice recordings) is private to that student + admins."""
    if asset.uploaded_by_id is None:
        return False
    uploader = db.get(User, asset.uploaded_by_id)
    return uploader is not None and uploader.role == UserRole.STUDENT


def can_view(db: Session, user: User, asset: MediaAsset) -> bool:
    if user.role == UserRole.ADMIN:
        return True
    if is_private_recording(db, asset):
        return asset.uploaded_by_id == user.id
    return asset.status == MediaStatus.READY


def media_url(asset_id: uuid.UUID | None) -> str | None:
    if asset_id is None:
        return None
    return f"{get_settings().api_prefix}/media/{asset_id}"
