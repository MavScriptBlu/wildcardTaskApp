"""

Alembic reads this file to figure out how to connect to the database
and what our tables are supposed to look like, so it can generate and run migrations.

"""

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Make sure Python can find our "app" package when this file runs on its own.
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

# Alembic loads this file as a standalone script, not as part of a package, so
# these have to be absolute imports rather than relative ones.
from app.database import Base
from app.models import Task  # noqa: F401 (import so Base knows about this table)

# Grab the database URL from the environment instead of alembic.ini, so this
# works the same in the container or on your machine.
config = context.config
db_url = os.getenv("DATABASE_URL", "postgresql://taskuser:taskpass@localhost:5432/taskdb")
config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic what our tables are supposed to look like, so it can compare
# that against the real database when generating migrations.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Generate migration SQL without an active database connection."""
    # Just need the URL for the SQL comments Alembic writes, not a real connection.
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a live connection to the database (the normal case)."""
    # Build a throwaway engine just for running the migration, no connection pooling needed.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Pick offline mode (just print SQL) or online mode (actually connect and run it),
# depending on how Alembic was invoked.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()