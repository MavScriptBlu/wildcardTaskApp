#! /usr/bin/env bash
# This script is used to run the development server for the project.
# Starts the backend and frontend together for local dev
# Ctrl+C stops both at once
#
# Assumes the db container is already running (podman compose up db,
# or your test-db container)

# load pyenv manually, since this script doesn't run throught normal
# interactive shell (so .zshrc doesn't get messed up)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate task-app

if [ ! -f .env ]; then
    echo "dev.sh: .env not found - cp .env.example .env and fill in DB credentials" >&2
    exit 1
fi

# load the same credentials the db container was started with, so we don't
# drift out of sync with whatever's actually in .env
set -a
source .env
set +a

export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"

# apply any pending migrations before starting the backend, so a fresh or
# updated db container doesn't 500 on first request
(cd backend && alembic upgrade head) || {
    echo "dev.sh: alembic upgrade head failed - is the db container running? (podman compose -f container-compose.yml up db)"
    exit 1
}

# start the backend, remember its process id so we can stop it later
(cd backend && uvicorn app.main:app --reload) & BACKEND_PID=$!

# start the frontend, remember its process id too
(cd frontend && npm run dev) & FRONTEND_PID=$!

# when you hit Ctrl+C, stop both processes
trap "kill $BACKEND_PID $FRONTEND_PID" INT TERM

wait