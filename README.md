# Task App

A simple task manager with a y2k vibe. Create, view, update, and delete tasks. Runs entirely in containers.

## Stack

- Frontend: SvelteKit + TypeScript
- Backend: FastAPI
- Database: PostgreSQL, schema managed with Alembic
- Containerization: Podman

---

## Project Structure

```structure
task-app/
├── backend/                # FastAPI app + Alembic migrations
│   ├── app/                 # API source (routers, models, schemas, config)
│   ├── alembic/              # Migration environment + versions
│   └── Containerfile        # Backend container image
├── frontend/               # SvelteKit + TypeScript app
│   ├── src/routes/          # Pages
│   └── src/lib/              # API client, types, components, styles
├── container-compose.yml   # Podman Compose file for running the app
├── dev.sh                   # Runs backend + frontend together for local dev
├── .env.example            # Template for required environment variables
├── README.md               # Project documentation
└── CHANGELOG.md            # Project changelog
```

---

## Development Environment Setup

This installs pyenv (lets you manage multiple Python versions) and the pyenv-virtualenv plugin (lets you make isolated Python environments per project).
Assumes zsh.

```bash
# install pyenv + pyenv-virtualenv
curl https://pyenv.run | bash
```

```bash
# add pyenv to your shell so it loads every time you open a terminal
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
```

```bash
# reload your shell so the changes actually take effect
source ~/.zshrc
```

You'll also need Podman and Node.js (v20+).

Both of the setups below share one file: copy `.env.example` to `.env` in the project root and fill in DB credentials. It's read by Podman Compose (containerized DB) and by `dev.sh` (local backend), so whatever you put there is what both sides will use to authenticate.

```bash
cp .env.example .env   # fill in DB credentials
```

---

## Option A: Run everything in containers

```bash
podman compose -f container-compose.yml up --build
```

This brings up Postgres, the backend (`:8000`), and the frontend (`:3000`). Environment variables for the database come from `.env`. The backend container runs `alembic upgrade head` before starting the API, so a fresh database gets its schema created automatically - no manual migration step needed.

This is the quickest way to get the whole app running, but the backend and frontend won't hot-reload on code changes - use Option B for active development.

## Option B: Run locally with hot-reload

The database still runs in a container; the backend and frontend run directly on your machine so you get hot-reload.

### 1. Start the db container

```bash
podman compose -f container-compose.yml up db
```

Leave this running in its own terminal (or use your own test DB, as long as its credentials match `.env`).

### 2. One-time backend setup

```bash
cd backend
pyenv virtualenv 3.12.4 task-app   # if you haven't already
pyenv local task-app
pip install -r requirements.txt
```

Apply the schema to the db container from step 1 (same credentials `dev.sh` uses, loaded from `.env`):

```bash
set -a && source ../.env && set +a
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
alembic upgrade head
```

### 3. One-time frontend setup

```bash
cd frontend
npm install
```

### 4. Run backend + frontend together (`dev.sh`)

From the project root, with the db container from step 1 still running:

```bash
./dev.sh
```

`dev.sh` loads the DB credentials from `.env`, runs `alembic upgrade head` (so a fresh or recreated db container gets its schema applied automatically), then starts the backend and frontend together. Ctrl+C stops both at once.

- Backend comes up on `http://localhost:8000`. `/health` is a liveness check; `/` is just a landing route.
- Frontend comes up on the port Vite prints (typically `http://localhost:5173`).
