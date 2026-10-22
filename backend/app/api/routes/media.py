import uuid

from fastapi import APIRouter, File, Form, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select

from app.api.deps import AdminUser, CurrentUser, DbSession
from app.core.errors import AppError
from app.models import MediaAsset, StoryEpisode
from app.models.enums import MediaStatus, MediaType
from app.schemas.common import Page
from app.schemas.curriculum import EpisodeMediaSet, EpisodeOut, MediaAdminView
from app.services import audit
from app.services import media as media_service
from app.storage import get_storage

router = APIRouter(tags=["media"])


@router.get("/media/{asset_id}", response_class=FileResponse)
def download_media(asset_id: uuid.UUID, db: DbSession, user: CurrentUser):
    """Authorised download/streaming (supports HTTP Range for audio/video seeking)."""
    asset = db.get(MediaAsset, asset_id)
    if asset is None or not media_service.can_view(db, user, asset):
        raise AppError(404, "Media not found.")
    path = get_storage().local_path(asset.storage_key)
    if path is None:
        raise AppError(404, "Media file is not available.")
    return FileResponse(
        path,
        media_type=asset.mime_type,
        headers={
            "Cache-Control": "private, max-age=3600",
            "X-Content-Type-Options": "nosniff",
            "Content-Disposition": "inline",
        },
    )


admin = APIRouter(prefix="/admin", tags=["admin: media"])


def _admin_view(asset: MediaAsset) -> MediaAdminView:
    return MediaAdminView.model_validate(asset)


@admin.post("/media", response_model=MediaAdminView, status_code=status.HTTP_201_CREATED)
def upload_media(
    db: DbSession,
    user: AdminUser,
    file: UploadFile = File(...),
    media_type: MediaType = Form(...),
    alt_text: str | None = Form(default=None, max_length=255),
    transcript: str | None = Form(default=None, max_length=20000),
):
    asset = media_service.store_upload(
        db,
        uploader=user,
        filename=file.filename or "upload",
        stream=file.file,
        media_type=media_type,
        alt_text=alt_text,
        transcript=transcript,
    )
    audit.record(
        db,
        user.id,
        "media.upload",
        "media_asset",
        asset.id,
        {"type": media_type, "filename": asset.original_filename, "size": asset.size_bytes},
    )
    db.commit()
    return _admin_view(asset)


@admin.get("/media", response_model=Page[MediaAdminView])
def list_media(
    db: DbSession,
    _: AdminUser,
    media_type: MediaType | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    # Student voice recordings are private learning data, not content assets.
    from app.models import User
    from app.models.enums import UserRole

    stmt = (
        select(MediaAsset)
        .outerjoin(User, User.id == MediaAsset.uploaded_by_id)
        .where((User.role == UserRole.ADMIN) | (MediaAsset.uploaded_by_id.is_(None)))
    )
    if media_type:
        stmt = stmt.where(MediaAsset.media_type == media_type)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(
        stmt.order_by(MediaAsset.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    return Page(items=[_admin_view(a) for a in items], total=total, page=page, page_size=page_size)


@admin.get("/media/{asset_id}", response_model=MediaAdminView)
def get_media(asset_id: uuid.UUID, db: DbSession, _: AdminUser):
    asset = db.get(MediaAsset, asset_id)
    if asset is None:
        raise AppError(404, "Media not found.")
    return _admin_view(asset)


def _require_asset(db: DbSession, asset_id: uuid.UUID | None, kind: MediaType) -> None:
    if asset_id is None:
        return
    asset = db.get(MediaAsset, asset_id)
    if asset is None or asset.media_type != kind or asset.status != MediaStatus.READY:
        raise AppError(422, f"Asset {asset_id} is not a ready {kind.value.lower()} file.")
    if media_service.is_private_recording(db, asset):
        raise AppError(422, "Student recordings cannot be attached to lessons.")


@admin.put("/episodes/{episode_id}/media", response_model=EpisodeOut)
def set_episode_media(episode_id: uuid.UUID, body: EpisodeMediaSet, db: DbSession, user: AdminUser):
    """Attach (or detach with null) the cartoon video, subtitles and poster of an episode."""
    episode = db.get(StoryEpisode, episode_id)
    if episode is None:
        raise AppError(404, "Episode not found.")
    _require_asset(db, body.video_asset_id, MediaType.VIDEO)
    _require_asset(db, body.subtitle_asset_id, MediaType.SUBTITLE)
    _require_asset(db, body.poster_image_id, MediaType.IMAGE)
    episode.video_asset_id = body.video_asset_id
    episode.subtitle_asset_id = body.subtitle_asset_id
    episode.poster_image_id = body.poster_image_id
    audit.record(
        db,
        user.id,
        "episode.media_set",
        "story_episode",
        episode.id,
        body.model_dump(mode="json"),
    )
    db.commit()
    return EpisodeOut(
        id=episode.id,
        title=episode.title,
        synopsis=episode.synopsis,
        position=episode.position,
        video_asset_id=episode.video_asset_id,
        subtitle_asset_id=episode.subtitle_asset_id,
        poster_image_id=episode.poster_image_id,
        has_video=episode.video_asset_id is not None,
    )
