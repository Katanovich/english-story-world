# 🌍 English Story World

An English-learning platform for children (CEFR **A1 → C1**). Learners follow two cartoon
characters, **Alex and Mia**, through short illustrated stories, listening dialogues, word
games, speaking practice and quizzes. Every lesson reuses earlier material, and a spaced-
repetition review queue brings words back at the right time.

Level **A1 is complete**: 10 lessons in two units ("Little Explorers" and "Our Big Family").
Levels A2–C2 are being written; see [COURSE_PLAN.md](COURSE_PLAN.md).

| For learners (English UI) | For teachers / admins (Russian UI) |
|---|---|
| Dashboard with the next lesson and real progress | Student accounts: create, suspend, restore, reset password |
| Step-by-step lesson player (words → reading → listening → sentences → speaking → quiz) | Course → level → unit → lesson editor |
| 10 exercise types, all checked on the server | Exercise editor with answer keys, hints and linked words |
| Voice recording and replay (never auto-graded) | Validation before publishing, preview as a student |
| Review queue, "My words" mastery, cartoon episodes | Media library (images, audio, video, subtitles), audit log |

> **Status:** working MVP. See [Known limitations](#-known-limitations) and [PLAN.md](PLAN.md).

---

## 📑 Contents

1. [Run it in 3 steps (Docker)](#-run-it-in-3-steps-docker)
2. [First steps in the app](#-first-steps-in-the-app)
3. [Why the GitHub link alone does not run the app](#-why-the-github-link-alone-does-not-run-the-app)
   · [Share it from your own computer (free)](#-share-it-from-your-own-computer-free)
4. [Local development (without Docker)](#-local-development-without-docker)
5. [Tests and checks](#-tests-and-checks)
6. [Project structure](#-project-structure)
7. [How it works](#-how-it-works)
8. [Security and privacy](#-security-and-privacy)
9. [Configuration (.env)](#-configuration-env)
10. [Known limitations](#-known-limitations)
11. [Troubleshooting](#-troubleshooting)

---

## 🚀 Run it in 3 steps (Docker)

**You need:** [Git](https://git-scm.com/downloads) and
[Docker Desktop](https://www.docker.com/products/docker-desktop/) (running).
Nothing else; Python, Node and PostgreSQL run inside containers.

```bash
# 1. Download the code
git clone https://github.com/Katanovich/english-story-world.git
cd english-story-world

# 2. Create your private settings file (random passwords are generated for you)
./scripts/setup-env.sh
#    → prints the admin login and password (also saved in .env)

# 3. Start everything (the first build takes a few minutes)
docker compose up --build
```

Then open **http://localhost:3000** and log in with the admin account printed in step 2.

On start, the backend container automatically:
1. creates or updates the database tables (Alembic migrations),
2. creates the admin account from `.env` (only if it does not exist),
3. loads the "Little Explorers" lessons (safe to repeat, never creates duplicates).

| Address | What |
|---|---|
| http://localhost:3000 | The app (learners and admins) |
| http://localhost:8000/docs | Interactive API documentation (OpenAPI / Swagger) |
| http://localhost:8000/api/v1/health | Health check |

Stop with `Ctrl+C`, or with `docker compose down` when running in the background
(`docker compose up -d --build`). Your data is kept in a Docker volume. To delete
everything, including the database, run `docker compose down -v`.

**Windows:** run step 2 in *Git Bash* or *WSL*. You can also do it by hand: copy
`.env.example` to `.env`, then set `POSTGRES_PASSWORD` (and the same password inside
`DATABASE_URL`), `SECRET_KEY`, `ADMIN_USERNAME` and `ADMIN_PASSWORD`. The admin password
needs at least 12 characters with letters and numbers.

---

## 👣 First steps in the app

1. **Log in as admin** → you land on the Russian admin dashboard (`/admin`).
2. **Ученики → Новый ученик**: create a student, e.g. login `sasha`, name `Sasha`, with a
   password. Leave the password empty to get a one-time invite code instead; the child enters
   it at `/reset-password`.
3. Open the student → **Курс и уровень** → choose *English Story World*, level *A1* →
   **Назначить**.
4. **Log out**, then log in as the student → the dashboard shows *Meet My Family* → **Start**.
5. Back as admin: watch the student's progress, word mastery and answers; edit lessons in
   **Курсы и уроки**; preview any lesson with **Просмотр как ученик**.

---

## 🔗 Why the GitHub link alone does not run the app

GitHub **stores and shows the code**. It cannot run a backend server or a database, so
opening the repository link shows the files, not the app. To use the app you either:

- **Run it on your computer** with the 3 steps above (recommended for testing), or
- **Deploy it to a server** to get a public web address. Any host that runs Docker Compose
  works: a small VPS (Hetzner, DigitalOcean, etc.) or a platform such as Render or Railway
  (backend + PostgreSQL + frontend as separate services). Before going public, follow the
  [production checklist](#production-checklist).

---

## 🌐 Share it from your own computer (free)

Your computer can act as the server through a free **Cloudflare quick tunnel**. No router
setup and no purchase are needed, and you get a public **HTTPS** link.

```bash
brew install cloudflared            # once (macOS); other systems: see Cloudflare's docs
# In .env set APP_ENV=production    # secure cookies when served over HTTPS
./scripts/share-online.sh
#  → Your app is online at: https://some-random-words.trycloudflare.com
```

Send that link to your students. Keep the Terminal window open; `Ctrl+C` stops sharing.
The script also keeps the Mac awake while the tunnel is open.

Good to know:
- **The link changes every time** you restart the script. A permanent link needs a
  free Cloudflare account plus your own domain (named tunnel).
- The app is online **only while your computer is on, awake and connected**. Closing the lid
  usually puts a laptop to sleep.
- Data lives on your computer: back it up, e.g.
  `docker compose exec db pg_dump -U esw english_story_world > backup.sql`.
- Only the tunnel is public. Docker publishes the ports on `127.0.0.1` only, so others
  on your Wi-Fi cannot reach the database or the API directly.
- With `APP_ENV=production`, use **Chrome, Edge or Firefox** for `http://localhost:3000`.
  Safari may refuse secure cookies on plain `http://localhost`; the HTTPS tunnel link
  works everywhere.
- For many students or everyday use, a small rented server is more reliable.

---

## 🛠 Local development (without Docker)

Run the database in Docker and the backend and frontend directly on your machine, with
hot reload. You need **Python 3.12+** and **Node.js 20+**.

```bash
./scripts/setup-env.sh                 # once
docker compose up -d db                # PostgreSQL on localhost:5434

# Backend: http://localhost:8000
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/alembic upgrade head
.venv/bin/python -m app.cli create-admin
.venv/bin/python -m app.cli seed
.venv/bin/uvicorn app.main:app --reload

# Frontend: http://localhost:3000 (in a second terminal)
cd frontend
npm install
npm run dev
```

The browser only talks to the Next.js address. Requests to `/api/v1/*` are forwarded to
FastAPI (`BACKEND_URL`, default `http://localhost:8000`), so the login cookie stays first-party.

**Management commands** (in `backend/`):

| Command | Effect |
|---|---|
| `python -m app.cli create-admin` | Create the admin from `ADMIN_*` in `.env` (never overwrites, never promotes a student) |
| `python -m app.cli seed` | Load the A1 lessons; existing records, including CMS edits, are left untouched |
| `python -m app.cli seed --update` | Re-apply the original seed content; changed items get new version numbers |

In Docker: `docker compose exec backend python -m app.cli <command>`.

---

## ✅ Tests and checks

```bash
# Backend: 81 tests against a real PostgreSQL test database (created automatically)
cd backend
.venv/bin/pytest
.venv/bin/ruff check .

# Frontend
cd frontend
npx tsc --noEmit
npm run lint
npm run build
```

The backend tests cover:
- login, sessions, logout, expiry and throttling;
- role checks: students cannot use admin endpoints, and one student cannot read another's data;
- suspension blocking access immediately;
- server-side scoring, with answer keys never sent before an answer;
- saved attempts and exercise versions, and progress surviving logout;
- the review schedule, and mastery rules;
- upload type, size and authorisation checks, and video attachment not breaking lessons;
- the CMS and its pre-publish validation;
- the seed: it can be rerun, and every one of the 80 seeded answer keys scores correctly through the API.

---

## 📁 Project structure

```
english-story-world/
├── docker-compose.yml        # db (PostgreSQL 16) + backend (FastAPI) + frontend (Next.js)
├── .env.example              # all settings, no secrets
├── scripts/setup-env.sh      # generates .env with random secrets
├── PLAN.md                   # build plan and status of each part
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app, middleware, routers
│   │   ├── cli.py            # create-admin, seed
│   │   ├── core/             # settings, password hashing, errors, middleware
│   │   ├── models/           # SQLAlchemy 2 models (users, curriculum, progress, media)
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── api/routes/       # auth, learning, media, admin_* routes
│   │   ├── services/         # auth, curriculum, progress, learning (SRS), media, publishing
│   │   ├── exercises/        # exercise definitions + server-side scoring
│   │   ├── storage/          # storage adapter (local now, S3 planned)
│   │   └── seed/             # "Little Explorers" content + idempotent seed runner
│   ├── alembic/              # database migrations
│   └── tests/                # pytest suite
└── frontend/
    └── src/
        ├── app/              # pages: /login, /learn/*, /admin/*
        ├── components/       # UI kit, lesson player, exercise renderers, recorder, admin forms
        └── lib/              # API client, auth context, types
```

---

## 🧠 How it works

### Architecture
A **modular monolith**: one FastAPI backend (REST under `/api/v1`), one Next.js frontend
(App Router, TypeScript, Tailwind) and PostgreSQL. There are no microservices.

### Curriculum
`Course → Level (A1…C1) → Unit → Lesson → Exercises + Learning items`. Lessons are **data**,
not hard-coded pages: reading passages, listening dialogues and grammar notes are stored as
validated JSON. Exercises are rows with a public `prompt` and a private `answer`. New
lessons are added in the admin CMS without code changes. Only A1 has content so far; the
other levels are supported by the data model and can be created in the CMS.

### Characters (your own family's names)
Stories use placeholders such as `{boy}`, `{little}` and `{gran1}`. The public code ships
neutral default names (Alex, Mia, Kate, …). To use your own family's names, create
`backend/app/seed/characters.local.json`. This file is git-ignored and never uploaded:

```json
{"boy": "Alex", "little": "Mia", "teen": "Kate", "dad": "Tom", "mum": "Anna",
 "gran1": "Rose", "gran2": "Lily", "aunt": "Emma"}
```

Replace the values with your names (one word each, Latin letters). Then run
`docker compose up -d --build backend && docker compose exec backend python -m app.cli seed --update`.

### Cumulative learning
Each **learning item** (word, phrase or grammar pattern) has a stable key. Every lesson marks
its items as **NEW**, **RECENT_REVIEW** (previous lesson) or **OLDER_REVIEW**. The seed works
these roles out from what each lesson actually practises. Lesson 5's quiz covers all five
lessons.

### Exercise engine
There are 10 types: multiple choice, picture choice, matching, sentence builder, fill in the
blank, reading comprehension, listening comprehension, true/false, story order, and speaking.

- All scoring happens on the server. Answer keys are never sent to the browser before the
  learner answers.
- The solution is shown after a correct answer, or after two wrong tries.
- Speaking is recorded and replayed only. It is **never** automatically graded.

### Mastery ≠ completion
- A lesson is *completed* when every activity has been tried.
- A word is *mastered* (score ≥ 0.8) only with both **recognition** evidence (choosing,
  matching) and **productive recall** (building, typing), weighted by accuracy. One correct
  picture click gives about 0.13.
- Instant retries within 10 minutes after feedback do not count as new evidence.

### Review queue (simplified SM-2)
- Correct → review again in 1 day, then 3 days, then the interval × an "ease" factor that slowly grows.
- Wrong → review again in 10 minutes, and the ease factor drops.

See `backend/app/services/learning.py`.

### Versioning and history
Changing an exercise's question, answer or points creates a new exercise version. Editing a
published lesson increases its content version. Each saved answer stores the version and a
snapshot of the exercise, so old results stay meaningful. Exercises that students have
answered cannot be deleted, and student learning records are never hard-deleted.

### Media and future cartoons
File metadata lives in PostgreSQL; the files themselves live in a **storage adapter**
(local disk now, outside the web root and git-ignored).

- Uploads are checked by extension **and** by file content, and SVG is rejected.
- Each file type has a size limit.
- Downloads require login and support seeking in audio and video.
- Each lesson has a story episode. Without a video it shows *"Cartoon coming soon"*. When
  the cartoons are ready, upload the MP4/WebM file and a WebVTT subtitle file, then attach
  them in the lesson's **Эпизоды и видео** tab. No code changes are needed.

---

## 🔒 Security and privacy

- **Passwords:** hashed with **Argon2id**, never stored or logged in plain text. There are
  no default credentials; the admin is created from `.env`.
- **Sessions:**
  - a random token in an **HttpOnly, SameSite=Lax** cookie (`Secure` in production);
  - only its SHA-256 hash is stored, so sessions can be revoked;
  - suspending a student or changing a password logs out all of that account's sessions immediately.
- **Authorisation:** checked on the server on every request.
  - Roles are `ADMIN` and `STUDENT`. Students cannot register themselves or change their role.
  - Every student-specific query is limited to the logged-in user.
  - Unpublished or other-course lessons return 404.
- **CSRF:** SameSite cookies plus a check of the request's origin on every change.
- **Brute force:** failed logins are throttled.
- **Errors and logs:** validation errors never echo submitted values, and request logs
  contain only the method, path, status and time.
- **Children's data:**
  - Only a username and display name are required; email is optional.
  - Voice recordings are private (visible only to the student and admins) and are never sent
    to external services.
  - There are no public profiles, leaderboards or streaks.
- **"Listen" buttons** use the browser's built-in speech synthesis until real recordings are
  uploaded, and say so on screen. Some browsers use an online voice service for this. Only
  lesson text is spoken, never personal data.

### Production checklist
- [ ] Set `APP_ENV=production` (secure cookies, no development-only reset-token logging).
- [ ] Use strong unique values for `SECRET_KEY`, `POSTGRES_PASSWORD` and `ADMIN_PASSWORD`, and
      remove `ADMIN_PASSWORD` from the environment after the first start.
- [ ] Serve over **HTTPS** behind a reverse proxy (nginx or Caddy). Set
      `CORS_ORIGINS` to your domain and an upload size limit (`client_max_body_size`).
- [ ] Do not publish ports 5434 (database) or 8000 (backend); only the frontend needs to be public.
- [ ] Set up an email provider for password resets (see below) and database backups.
- [ ] Set `SEED_ON_START=false` once the content is managed in the CMS.

---

## ⚙️ Configuration (.env)

| Variable | Meaning |
|---|---|
| `APP_ENV` | `development` or `production` |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Database credentials (container) |
| `POSTGRES_HOST_PORT` | Database port on your computer (default 5434) |
| `DATABASE_URL` | Backend connection string for local development (Docker overrides the host) |
| `TEST_DATABASE_URL` | Database used by pytest (created and dropped automatically) |
| `SECRET_KEY` | Long random secret |
| `SESSION_TTL_HOURS` | Login session lifetime (default 72) |
| `CORS_ORIGINS` | Allowed frontend origins, comma-separated |
| `ADMIN_EMAIL`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` | Initial admin (created once) |
| `SEED_ON_START` | `true`: load the A1 lessons when the backend container starts |
| `STORAGE_BACKEND`, `LOCAL_STORAGE_DIR` | Media storage (`local` only for now) |
| `MAX_IMAGE_MB`, `MAX_AUDIO_MB`, `MAX_VIDEO_MB` | Upload size limits |

---

## ⚠️ Known limitations

This is an honest list of what is not done yet.

- **No cartoon videos or recorded audio yet.** Emoji are used as illustrations, the browser
  voice is used for "Listen", and episodes show a placeholder. All of these are labelled in
  the UI.
- **Email is not configured.** A password-reset request does not send an email; in
  development the code appears in the backend log. Admins can create reset codes for
  students in the dashboard.
- **S3 storage is designed but not implemented.** It is planned as a private bucket with
  short-lived signed upload and playback links; see `backend/app/storage/__init__.py`.
  There is no video transcoding or adaptive streaming.
- **No speech recognition.** Speaking practice is recorded and self-checked only.
- **Login throttling is in memory.** It works for one backend process; with several, use
  Redis or similar.
- **Some CMS fields are raw JSON.** Listening dialogues and grammar notes are edited as JSON,
  validated by the server.
- **Remaining from the build plan (Part 7):** automated frontend tests, a final security review.
- **Only A1 has content.** Levels A2–C1 can be created in the CMS but have no lessons yet.

---

## 🧯 Troubleshooting

| Problem | Fix |
|---|---|
| `port is already allocated` | Another program uses 3000, 8000 or 5434. Stop it, or change `POSTGRES_HOST_PORT` / the `ports` in `docker-compose.yml`. |
| `set POSTGRES_PASSWORD in .env` | You skipped step 2: run `./scripts/setup-env.sh`. |
| Cannot log in as admin | Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`, then look at `docker compose logs backend`. The admin is only created if it does not exist yet. |
| Student sees "No course yet" | Assign a course in the admin: Ученики → student → Курс и уровень. |
| Changed `.env` but nothing changed | Run `docker compose up -d --build` again. |
| Start completely fresh | `docker compose down -v` (deletes all data), then `docker compose up --build`. |
