import uuid

from sqlalchemy import BigInteger, CheckConstraint, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, Timestamps, UUIDPk, str_enum
from app.models.enums import MediaStatus, MediaType


class MediaAsset(UUIDPk, Timestamps, Base):
    """Metadata for an uploaded file. The binary lives in the storage backend, never here."""

    __tablename__ = "media_assets"
    __table_args__ = (CheckConstraint("size_bytes >= 0", name="size_non_negative"),)

    media_type: Mapped[MediaType] = mapped_column(
        str_enum(MediaType, "media_type"), nullable=False, index=True
    )
    storage_backend: Mapped[str] = mapped_column(String(32), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(127), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    status: Mapped[MediaStatus] = mapped_column(
        str_enum(MediaStatus, "media_status"), nullable=False, default=MediaStatus.PENDING
    )
    # For audio/video: an optional subtitle file (WebVTT) and/or plain transcript.
    subtitle_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )
    transcript: Mapped[str | None] = mapped_column(Text)
    alt_text: Mapped[str | None] = mapped_column(String(255))
    uploaded_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
