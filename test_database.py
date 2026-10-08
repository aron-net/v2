"""
BPU Nexus - Database Connection Test

Purpose:
    Verifies that BPU Nexus can connect to PostgreSQL
    using SQLAlchemy.

Why we have this file:
    We want to prove that the complete database connection
    works before building database models or API endpoints.

Connection flow:

    test_database.py
          ↓
    SQLAlchemy Engine
          ↓
    Psycopg Driver
          ↓
    PostgreSQL Docker Container

Security:
    We do not print the database password or DATABASE_URL.

If changing later:
    This test can be extended to verify additional database
    functionality.
"""

from sqlalchemy import text

from app.db.session import engine


def test_database_connection():
    """
    Test whether PostgreSQL is reachable.

    Returns:
        None

    Raises:
        Exception if the database connection fails.
    """

    # Open a database connection using SQLAlchemy.
    with engine.connect() as connection:

        # Execute a very small SQL query.
        #
        # SELECT 1 does not modify the database.
        # It simply proves that PostgreSQL accepted our
        # connection and can execute SQL.
        result = connection.execute(text("SELECT 1"))

        # Get the returned value.
        value = result.scalar()

        # Display the result so we can confirm the test worked.
        print("Database connection successful.")
        print("PostgreSQL response:", value)


# Run the test when this file is executed directly.
if __name__ == "__main__":
    test_database_connection()