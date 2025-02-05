from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
import asyncio
from sqlalchemy.sql import text
# Import models and Base metadata
from app.models import Base, schemas  # Import the Base and schema list

# Get Alembic config
config = context.config

# Interpret config file for Python logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set metadata for Alembic to detect model changes
target_metadata = Base.metadata

# Database URL (should be set in alembic.ini)
DATABASE_URL = config.get_main_option("sqlalchemy.url")

def run_migrations_offline():
    """Run migrations in 'offline' mode without a DB connection."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    # Create async engine
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        future=True,
        echo=True  # Enable SQL logging
    )

    async with connectable.connect() as conn:
        # Create each schema with autocommit
        for schema in schemas:
            await conn.execute(
                text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"').execution_options(autocommit=True)
            )

        # Run migrations
        await conn.run_sync(do_run_migrations)

        # Explicitly commit the transaction
        await conn.commit()

    # Dispose of the engine
    await connectable.dispose()

def do_run_migrations(connection):
    """Apply migrations with an active connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
