"""
BPU Nexus - Database Session

Purpose:
    Creates the SQLAlchemy database engine and provides
    database sessions for the application.

Used by:
    FastAPI routes and services that need to read or write
    data in PostgreSQL.

Database flow:

    FastAPI
       ↓
    Service
       ↓
    Database Session
       ↓
    SQLAlchemy
       ↓
    Psycopg
       ↓
    PostgreSQL

Security:
    The database connection URL comes from application
    configuration. It is NOT hardcoded in this file.

If changing later:
    Database connection settings should normally be changed
    through .env and config.py rather than changing this file.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# ------------------------------------------------------------
# DATABASE ENGINE
# ------------------------------------------------------------

# The engine is SQLAlchemy's main connection manager.
#
# It knows:
#   - which database we are connecting to
#   - which database driver to use
#   - how to manage connections
#
# The actual DATABASE_URL comes from .env through settings.
engine = create_engine(
    settings.database_url,
)


# ------------------------------------------------------------
# DATABASE SESSION
# ------------------------------------------------------------

# sessionmaker creates database session objects.
#
# A session represents a unit of interaction with PostgreSQL.
#
# We will later use a session to:
#   - query records
#   - insert records
#   - update records
#   - delete records
#
# autocommit=False:
#   Changes are not automatically committed.
#   We explicitly decide when changes should be saved.
#
# autoflush=False:
#   SQLAlchemy will not automatically send pending changes
#   to PostgreSQL before every query.
#
# This gives us better control over database transactions.
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)