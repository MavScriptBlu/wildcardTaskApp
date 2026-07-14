# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versioning follows [SemVer](https://semver.org/).

## [Unreleased]

### Added

- SvelteKit + TypeScript frontend scaffold with dev/build/preview/check scripts.
- Frontend API client and shared task types (`src/lib/api.ts`, `src/lib/types.ts`).
- `TaskForm` and `TaskCard` components, plus global styles.
- Main task list page wired up to the API client.
- FastAPI backend with task CRUD routes, SQLAlchemy models, and Pydantic schemas.
- Alembic migration environment, including the initial `tasks` table migration.
- `.env.example` documenting required Postgres environment variables.
- `Containerfile` for the backend and frontend services.
- `container-compose.yml` to run Postgres, backend, and frontend together via Podman.
- `dev.sh` to run the backend and frontend together for local development outside containers, stopping both on Ctrl+C. Assumes the Postgres container is already running.

### Fixed

- Syntax error in the `DATABASE_URL` assignment in backend config.
- Container name and port formatting in `container-compose.yml`.
- Postgres healthcheck in `container-compose.yml` was missing `-d ${POSTGRES_DB}`, so `pg_isready` defaulted to a database named after the Postgres user (which doesn't exist) and never reported healthy, leaving `backend`'s `depends_on: condition: service_healthy` unable to proceed cleanly.
- Backend container never ran Alembic migrations, so a fresh Postgres volume had no `tasks` table and every API request failed with a 500 until someone ran `alembic upgrade head` by hand. The backend `Containerfile` now runs `alembic upgrade head` before starting `uvicorn`, so `podman compose up --build` initializes a fresh database on its own.
- `dev.sh` had the same gap as above for the local (non-containerized) dev workflow: it never ran migrations, so a fresh or recreated db container still hit the same "relation tasks does not exist" 500 even though the container path was fixed. `dev.sh` now runs `alembic upgrade head` before starting `uvicorn`, with a clear error if it fails (e.g. the db container isn't up).
- `dev.sh`'s `DATABASE_URL` assignment was never actually exported to the backend process (an `export` with no arguments on its own line, followed by a plain `VAR=value` assignment), so `uvicorn` only worked by coincidence because the backend's fallback default happened to match. Now exported properly, and set once up front for both the migration step and `uvicorn`.
