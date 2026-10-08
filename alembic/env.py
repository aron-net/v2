# ---------------------------------------------------------
# Alembic migration environment
# ---------------------------------------------------------
#
# This file connects Alembic to our SQLAlchemy application.
#
# Alembic uses this file to:
# 1. Connect to the PostgreSQL database.
# 2. Discover our SQLAlchemy models.
# 3. Compare models with the current database structure.
# 4. Generate database migrations.
# ---------------------------------------------------------

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import application settings.
# This allows Alembic to get DATABASE_URL from our .env file.
from app.core.config import settings

# Import our SQLAlchemy Base class.
#
# Base is important because it contains the metadata
# for all of our database models.
from app.db.base import Base

# Import every database model here.
#
# Alembic needs these imports so the models are registered
# inside Base.metadata.
#
# If we create more models later, for example:
#
#     User
#     Supplier
#     Procurement
#     PurchaseOrder
#
# we will import them here as well.
from app.models.user import User

# Import the Role model so Alembic knows about it.
from app.models.role import Role


# Get the Alembic configuration object.
#
# This comes from alembic.ini.
config = context.config


# Configure Python logging using the settings
# from alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ---------------------------------------------------------
# SQLAlchemy model metadata
# ---------------------------------------------------------
#
# Base.metadata contains information about all the tables
# defined by our SQLAlchemy models.
#
# Alembic uses this information when we run:
#
#     alembic revision --autogenerate
#
# For example, our User model will tell Alembic that
# a "users" table should exist.
target_metadata = Base.metadata


# ---------------------------------------------------------
# Database connection
# ---------------------------------------------------------
#
# We get the database URL from our application settings.
#
# The URL currently comes from .env:
#
# DATABASE_URL=postgresql+psycopg://...
#
# We do NOT put the database password directly inside
# alembic.ini.
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)

# ---------------------------------------------------------
# Offline migrations
# ---------------------------------------------------------
#
# Offline mode generates SQL without directly connecting
# to the database.
#
# This can be useful when we want to inspect the SQL
# that a migration would execute.
def run_migrations_offline() -> None:

    # Get the database URL from our application settings.
    url = settings.database_url

    # Configure Alembic for offline SQL generation.
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Run the migration inside a transaction.
    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# Online migrations
# ---------------------------------------------------------
#
# This is the normal mode we will use.
#
# Alembic connects directly to PostgreSQL and applies
# migration changes.
def run_migrations_online() -> None:

    # Create the SQLAlchemy database connection configuration.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Open a connection to PostgreSQL.
    with connectable.connect() as connection:

        # Tell Alembic which database connection and
        # SQLAlchemy metadata it should use.
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # Run migrations inside a transaction.
        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------
# Choose migration mode
# ---------------------------------------------------------
#
# Alembic can run either:
#
# - offline migrations
# - online migrations
#
# We automatically choose the correct function here.
if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()