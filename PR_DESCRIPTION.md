# PR: `fix/all-bugfixes` → `main`

Everything below is ready to copy-paste into GitHub.

---

## 1. PR TITLE

```
fix: backend startup crash, profile persistence, post submission, reactions, notifications, admin flow + Instagram-style posting & one-command setup
```

---

## 2. PR DESCRIPTION (paste into the PR body)

```markdown
## Summary

This PR repairs the backend (which could not start on `main`), fixes every
reported user-facing bug (profile fields disappearing on reload, post
submission 500s, dead reactions button, empty notifications, broken admin
dashboard, subscriptions CORS errors), adds Instagram-style post creation,
admin sign-up, and a one-command dev setup (`bash dev.sh`) that also
auto-repairs databases created from the old models.

Verified with **53 automated backend e2e checks** (`backend/e2e_test.py`)
and **37 frontend tests** — all passing — plus a full live run of both servers.

## What was broken

### Backend could not even start
- `app/__init__.py` imported `app.routes.auth` / `app.routes.users` which **do not exist** → `ModuleNotFoundError` on startup
- `ai_routes.py` lived in `app/Routes/` (capital R) but is imported lowercase → crashes on Linux/CI
- `auth_profile_bp` (login / register / forgot-password / `/me`) and `admin_bp` were **never registered** → all auth & admin endpoints 404
- `comments.py` / `comment_reactions.py` used `from app import db` → `ImportError`
- `run.py` called `create_app(config_name=…)` vs the factory's `config_class` → `TypeError`

### User-facing bugs
- **Skills & GitHub disappear on reload**: `GET /api/me` never returned them, and updates wrote GitHub to a non-existent column (`GithubProfile` instead of `GithubURL`) so it was silently never saved
- **Post submission failing (500)**: the `Content` status check-constraint didn't allow `Pending` (what new learner posts get); the create response had no `id` (frontend navigated to `/content/undefined`); uploads were saved to a folder Flask doesn't serve → media 404; `GET /api/content/<id>` returned `None` when content had no author
- **Reactions not working**: `ContentDetail` called `react(id, user.id, type)` — the user id was sent *as the reaction type* (400 every click); no GET summary endpoint existed; the POST returned no counts
- **Notifications dead**: `notifications.py` was a hardcoded `return []`; `_notify_subscribers()` in `content.py` was defined but **never called**; response keys didn't match what the page reads (`isRead` / `contentId` / `createdAt`)
- **Admin broken**: `role_required` read a role that isn't in the JWT → passed everyone through; dashboard's `adminApi` called `api.get()` on a fetch wrapper (TypeError) with wrong URLs; "Rejected" status violated the DB constraint (500); `RoleRoute` compared roles case-sensitively so real admins were locked out of `/admin`; `GET /api/reports` was unroutable
- **Subscriptions CORS error**: blueprint registered under `/api` with empty routes → `GET/POST /api/subscriptions` 404 → the OPTIONS preflight failed, which the browser reports as a CORS error
- **Misleading CORS errors on 500s**: unhandled exceptions in debug mode escalated to the Werkzeug debugger page, which carries **no CORS headers** — the browser showed "No 'Access-Control-Allow-Origin'" instead of the real error
- Wishlist remove sent the content id where the API expects the wishlist row id; search (`?q=`) was ignored by the content API

## What's new

- 📸 **Instagram-style composer** at `/create`: drag & drop image/video/audio with live preview, caption, auto-derived title, category chips, share confirmation ("live" vs "sent for review"); long-form editor (with AI helpers) moved to `/create-article`; optimistic ❤️ button on feed cards
- 👑 **Admin sign-up**: account-type picker (Learner / Tech Writer / Admin) on the sign-up page; roles normalised; admins land on `/admin`
- 🥬 **`bash dev.sh`** — one command: installs deps, prepares/migrates/seeds the DB (default admin `admin` / `Admin123!`), starts backend (5001) + frontend (5173)
- 🩺 **`app/schema_doctor.py`** — idempotent schema repair for databases created from old models (adds missing columns, allows `Pending` status, preserves data); runs automatically on dev-server boot and via `backend/setup_db.py`
- 🔔 Subscriber notifications fire when content is published (immediately for admin/tech_writer, or when an admin approves a pending post)
- Global JSON error handler keeps CORS headers on every error and returns an actionable "schema is out of date — run bash dev.sh" hint when drift is detected

## Database

- New migration `a1f2c3d4e5f6` (adds `content.RejectionReason`); model re-aligned with the migration history (`Summary`, `Duration`, `LikesCount`, `is_admin`)
- **No data loss**: old local databases are auto-repaired in place on first `bash dev.sh` / `python run.py`; existing users and posts are preserved

## How to test

```bash
bash dev.sh                                  # runs the whole stack
# login: admin / Admin123!  (or sign up a new Learner/Tech Writer/Admin)

cd backend && .venv/bin/python e2e_test.py   # 53 automated checks
cd ../client && npx jest                     # 37 frontend tests
```

Manual smoke test:
1. Sign up (pick **Admin**) → lands on `/admin`
2. Profile → add skills + GitHub URL → save → **reload** → both still there
3. `/create` → drag in a photo + caption → Share → post appears in the feed with the image served from `/static/uploads/...`
4. Heart a post from the feed and from the detail page → count updates, click again to unlike
5. As a learner, post something → it's "Pending"; as admin, approve it from `/admin` → the author gets a notification
6. Notifications page → list loads, "mark all as read" works

## Notes for reviewers

- All API changes are additive (extra fields / aliases like `id` + `content_id`, camelCase + snake_case) — existing consumers keep working
- `role_required` now actually enforces roles from the DB (case-insensitive): admin endpoints return 403 for non-admins (covered by e2e)
- Frontend base URL still `http://localhost:5001` (overridable via `VITE_API_BASE_URL`)
```

---

## 3. COMMIT MESSAGE

The branch has **4 commits** (see `git log main..fix/all-bugfixes`). If you merge
with **"Squash and merge"** (recommended), GitHub will ask for one commit
message — use this:

```
fix: repair backend startup, profile persistence, post submission, reactions, notifications, admin flow + Instagram-style posting & one-command setup

Backend could not start on main: phantom auth/users imports, unregistered
auth/admin blueprints, wrong-case Routes/ folder, and `from app import db`
ImportErrors. Beyond startup:

- Profile: /api/me returns skills + github_url; GitHub saved to the real
  GithubURL column (was silently lost) — fields no longer vanish on reload
- Posts: 'Pending' allowed by the status constraint (fresh-DB 500), uploads
  land in the servable static folder, response includes id, single-content
  GET fixed, search + case-insensitive status filter added
- Reactions: correct frontend call, GET summary endpoint, POST returns
  counts and toggles off on repeat; Instagram-style heart on feed cards
- Notifications: real endpoints (was hardcoded []), _notify_subscribers
  fires on publish/approval, camelCase keys
- Admin: blueprint registered, role checks enforced case-insensitively,
  Rejected mapped to Archived (constraint-safe), RejectionReason column +
  migration, dashboard API rewritten against real routes
- Subscriptions: registered at /api/subscriptions (was 404 -> CORS error)
- Errors: global JSON handler keeps CORS headers on 500s; schema drift
  returns an actionable hint
- DB: app/schema_doctor.py repairs old local databases idempotently and
  auto-runs on dev-server boot; dev.sh one-command stack; setup_db.py
- Frontend: account-type picker on signup (Learner / Tech Writer / Admin),
  case-insensitive RoleRoute, wishlist remove uses the row id

Verified: 53 backend e2e checks + 37 frontend tests, all passing.
```

---

## 4. HOW TO GET THIS INTO GITHUB

### Step 1 — apply the patch on your machine

Download **`fix-all.patch`** from the workspace, then:

```bash
cd cc2-moringa-daily-dev
git checkout main && git pull origin main
git checkout -b fix/all-bugfixes
git am --3way ~/Downloads/fix-all.patch
```

### Step 2 — push the branch

```bash
git push -u origin fix/all-bugfixes
```

### Step 3 — open the PR

Open:

```
https://github.com/mahneeofficial/cc2-moringa-daily-dev/compare/main...fix/all-bugfixes
```

(or GitHub shows a "Compare & pull request" button right after the push)
Paste section **2** as the description and create the PR.

### Step 4 — merge

Click **"Squash and merge"** and paste section **3** as the commit message.

### Step 5 — everyone else pulls the fix

```bash
git checkout main && git pull origin main && bash dev.sh
```

`bash dev.sh` repairs old local databases automatically on first run —
nobody needs to delete their `app.db` (delete it only if you want a
completely fresh seeded database).
