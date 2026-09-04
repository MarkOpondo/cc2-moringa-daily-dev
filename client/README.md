# Moringa Daily Dev

A full-stack developer community platform built with React, Vite, Tailwind CSS, Flask, and PostgreSQL (or SQLite for local development).

## Project structure

```text
cc2-moringa-daily-dev/
├── backend/  # Flask API and database migrations
└── client/   # React frontend
```

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
. .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

The API defaults to SQLite at `backend/instance/moringa_daily_dev.sqlite3`. To use PostgreSQL, set either `DATABASE_URL` or the documented `DB_*` variables:

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/moringa_daily_dev
SECRET_KEY=replace-with-a-long-random-value
JWT_SECRET_KEY=replace-with-a-different-long-random-value
FRONTEND_URL=http://localhost:5173
```

Run the API:

```bash
python run.py
```

The API listens on `http://localhost:5001` by default. Run database migrations when using an existing database:

```bash
flask --app run.py db upgrade
```

Seed data is an explicit operation and is not run automatically when the server starts:

```bash
python -m app.seed
```

### Frontend

```bash
cd client
npm install
npm run dev
```

The Vite development server proxies `/api` requests to `http://localhost:5001`. Set `VITE_API_PROXY_TARGET` to point to another local API. For production, set `VITE_API_BASE_URL` to the public API origin if the API is hosted separately.

## Canonical API conventions

- JSON uses camelCase fields (`categoryId`, `createdAt`, `mediaUrl`).
- Content types are `article`, `video`, `audio`, or `image`.
- Content statuses are `draft`, `published`, or `archived`.
- Public content endpoints return only approved published content.
- Admin endpoints are grouped under `/api/admin`.
