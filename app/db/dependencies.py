# ---------------------------------------------------------
# Database Dependencies
# ---------------------------------------------------------
#
# This file provides database sessions to our FastAPI
# endpoints.
#
# Instead of creating a new database connection manually
# inside every API endpoint, FastAPI will provide a
# SQLAlchemy session for us.
#
# The session is automatically closed after the request
# finishes.
# ---------------------------------------------------------

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Create a database session for a FastAPI request.

    The session is yielded to the endpoint and then closed
    automatically when the request is finished.
    """

    # Create a new SQLAlchemy database session.
    db = SessionLocal()

    try:
        # Give the database session to the API endpoint.
        yield db

    finally:
        # Always close the session after the request.
        #
        # This prevents unused database connections from
        # remaining open.
        db.close()
