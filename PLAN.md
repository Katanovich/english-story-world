# English Story World — Build Plan

The full product brief is implemented in 7 parts. Each part ends in a stable,
tested state. A new session should read this file first, then continue with
the first part that is not marked DONE.

| Part | Scope | Status |
|------|-------|--------|
| 1 | Repo skeleton, Docker Compose + PostgreSQL, FastAPI app, full DB schema, Alembic initial migration, first tests | DONE |
| 2 | Auth (argon2 hashing, HttpOnly cookie sessions), roles, account statuses, admin bootstrap command, password reset (dev fallback), auth/authorization tests | DONE |
| 3 | Curriculum API, exercise engine (server-side scoring, answers hidden), lesson progress, spaced-repetition review queue, media storage adapter + uploads, tests | DONE |
| 4 | "Little Explorers" A1 content: 5 lessons, learning items, exercises, cumulative review links; idempotent seed script; content tests | DONE |
| 5 | Next.js frontend: design system, login, student dashboard, lesson player for all exercise types, recording, media placeholders | DONE |
| 6 | Admin dashboard + CMS: students, content/exercise editing, media upload/attach, preview, publish validation, audit log | DONE |
| 7 | Frontend tests, lint, typecheck, production build, full Docker run, security review, final README / architecture / limitations | TODO |

## Key decisions (keep consistent across parts)

- Modular monolith: `backend/` (FastAPI, SQLAlchemy 2, Alembic, PostgreSQL), `frontend/` (Next.js App Router, TypeScript).
- All primary keys are UUIDs. Enums are stored as VARCHAR + CHECK (`native_enum=False`) so they are easy to extend.
- Lesson rich content (reading passage, listening dialogues, speaking prompts) lives in `lessons.content` (JSONB) validated by Pydantic schemas; exercises are rows in `exercises` with `prompt` (public) and `answer` (private) JSONB.
- Versioning: `lessons.content_version` and `exercises.version` are bumped on edit/publish; each `exercise_attempts` row stores `exercise_version` plus a snapshot of the exercise so history stays interpretable.
- Auth: opaque random session token in an HttpOnly cookie; only its SHA-256 hash is stored (`auth_sessions`). Suspension revokes access immediately.
- Mastery (`learner_mastery`) is separate from scheduling (`review_queue`). Recognition and recall are counted separately.
- Media binaries are never stored in PostgreSQL; `media_assets` holds metadata and a storage key. Storage is behind an adapter (local now, S3-compatible later).
- Local dev: PostgreSQL runs in Docker on host port **5434**. Backend venv at `backend/.venv` (Python 3.13).

## Dev commands

```bash
docker compose up -d db                    # start PostgreSQL
cd backend && source .venv/bin/activate
alembic upgrade head                       # apply migrations
uvicorn app.main:app --reload              # API at http://localhost:8000/api/v1, docs at /docs
pytest                                     # tests (uses the test database)
```

## Implemented API so far (Part 2)

- `POST /auth/login` `POST /auth/logout` `GET /auth/me` `POST /auth/change-password`
- `POST /auth/password-reset/request` (always 202; dev: token logged to server console) `POST /auth/password-reset/confirm`
- `GET/POST /admin/students`, `GET/PATCH /admin/students/{id}`, `POST /admin/students/{id}/status`, `POST /admin/students/{id}/password-reset` (returns one-time token to admin)
- Deps: `CurrentUser`, `AdminUser`, `StudentUser` in `app/api/deps.py`; errors via `AppError` → `{"error": {code, message, details}}`; audit via `app/services/audit.record`.
- Tests: fixtures `login_as`, `make_user`, `new_client`, `db` in `tests/conftest.py`; tables truncated after each test.

## Implemented in Part 3

- Exercise engine: `app/exercises/definitions.py` (per-type prompt/answer/response schemas,
  `validate_definition` — use it in seed + CMS), `app/exercises/scoring.py` (server scoring).
  Formats: choice types `{question, options[{id,text|image_id}]}` / `{correct}`; TRUE_FALSE
  `{statement}` / `{correct: bool}`; MATCHING `{left, right}` / `{pairs}`; SENTENCE_BUILDER
  `{tiles}` / `{accepted}`; FILL_BLANK `{text with ___, word_bank}` / `{blanks: [[...]]}`;
  ORDER_EVENTS `{items}` / `{order}`; SPEAKING `{text, model_answer}` / `{}` (never auto-scored).
  Feedback JSON: `{correct, incorrect, hint, explanation}`.
- Lesson content JSON schema: `app/schemas/content.py` (`LessonContent`: story_intro, reading, listening[], grammar[]).
- Mastery + SM-2-lite scheduling: `app/services/learning.py` (documented in docstring).
- Progress: `app/services/progress.py` (lesson COMPLETED when every exercise attempted; enrollment advances).
- Storage adapter: `app/storage` (local implemented; S3 documented stub). Upload validation: `app/services/media.py`.
- Routes: `GET /lessons/{id}`, `POST /lessons/{id}/start`, `POST /exercises/{id}/attempts`,
  `GET /me/dashboard|courses|progress|review|attempts`, `POST /me/recordings`, `GET /media/{id}`,
  `POST/GET /admin/media`, `PUT /admin/episodes/{id}/media`, `PUT /admin/students/{id}/enrollment`,
  `GET /admin/students/{id}/progress`.
- Test helper: `tests/factories.py` (`build_world`, `enroll`).
- Not yet: admin CRUD for courses/units/lessons/items/exercises (Part 6).

## Implemented in Part 4

- Content: `backend/app/seed/little_explorers.py` (45 learning items, 5 lessons, 80 exercises, 5 episodes without video).
  Emoji (`Option.emoji`, `LearningItem.emoji`) are the illustrations until artwork exists.
  Listening prompts have `listen_text` (play audio_id if present, else browser speech synthesis — frontend Part 5).
  FILL_BLANK prompts may have `hint_ru`.
- Seed runner: `backend/app/seed/__init__.py` → `python -m app.cli seed [--update]`. Review roles are derived automatically.
- Dev DB is seeded. Tests: `tests/test_seed.py`.

## Implemented in Part 5

- `frontend/` Next.js 15.5 (App Router, TS, Tailwind v4). Browser calls same-origin `/api/v1/*`,
  proxied to FastAPI by `next.config.ts` rewrites (BACKEND_URL). `src/middleware.ts` = UX redirect only.
- `src/lib`: `api.ts` (fetch + ApiError), `useApi.ts`, `auth.tsx` (AuthProvider, useRequireRole), `types.ts`, `speech.ts`.
- `src/components`: `ui.tsx` (Button, Card, ProgressBar, Loading/Error/Empty states, Notice, Badge),
  `media.tsx` (Illustration, ListenButton, ListeningTrackPlayer, EpisodePlayer), `LessonPlayer.tsx`
  (supports `preview` prop for admin), `LessonSections.tsx`, `exercises/` (ExerciseCard, renderers, Recorder).
- Pages: `/`, `/login`, `/forgot-password`, `/reset-password`, `/learn` (dashboard), `/learn/lessons/[id]`,
  `/learn/review`, `/learn/progress`, `/learn/episodes`; `/admin` is a temporary placeholder (Part 6).
- Backend added `GET /me/episodes`.
- Verified manually in Chrome: login, dashboard, lesson start, matching (correct), image selection (wrong → hint), progress persists after reload.
- Dev demo student: username `demo`, password in `.env` (`DEMO_STUDENT_PASSWORD`), enrolled in A1.
- Frontend Dockerfile + compose service added, not yet built in Docker (Part 7).

## Implemented in Part 6

- Backend `app/api/routes/admin_content.py`: `/admin/overview`, `/admin/audit-logs`, `/admin/courses` (tree + create/patch),
  `/admin/courses/{id}/levels`, `/admin/levels/{id}` + `/units`, `/admin/units/{id}` + `/lessons`,
  `/admin/lessons/{id}` (GET full incl. answers, PATCH), `/validation`, `/publish`, `/unpublish`, `PUT /items`,
  `/admin/lessons/{id}/exercises` (POST), `/admin/exercises/{id}` (PATCH, DELETE only if no attempts),
  `/admin/lessons/{id}/episodes`, `/admin/episodes/{id}` (PATCH), `/admin/learning-items` (GET/POST/PATCH).
  Publish checks: `app/services/publishing.py` (Russian messages; errors block publish, warnings don't).
  Versioning: scoring-relevant exercise edits bump `exercise.version`; edits to a PUBLISHED lesson bump `content_version`.
- Frontend admin (Russian UI): `/admin` overview, `/admin/students` (+`[id]`: profile, status, reset code, enrolment,
  progress/mastery/attempts), `/admin/courses`, `/admin/lessons/[id]` (tabs: main, content, items, exercises, episodes;
  publication panel), `/admin/lessons/[id]/preview`, `/admin/items`, `/admin/media`, `/admin/audit`.
  Components: `src/components/admin.tsx`, `src/components/adminLesson/ExerciseEditor.tsx`; types `src/lib/adminTypes.ts`.
- Tests: `backend/tests/test_cms.py` (81 backend tests total). Verified in Chrome: admin login, course tree, lesson editor, exercise edit form, students list.
