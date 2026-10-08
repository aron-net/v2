# ---------------------------------------------------------
# Create a test user
# ---------------------------------------------------------
#
# This script inserts one test user into PostgreSQL.
#
# We are using SQLAlchemy rather than writing raw INSERT SQL.
# This keeps our application code consistent with our models.
# ---------------------------------------------------------

from app.db.session import SessionLocal
from app.models.user import User


def create_test_user():
    """
    Create one test user in the database.
    """

    # Open a database session.
    db = SessionLocal()

    try:
        # Create a new User object.
        user = User(
            name="Aron Test",
            email="aron.test@example.com",
            role="USER",
        )

        # Add the user to the current database transaction.
        db.add(user)

        # Save the transaction to PostgreSQL.
        db.commit()

        # Refresh the object so SQLAlchemy gets the
        # automatically generated ID and created_at values.
        db.refresh(user)

        print("Test user created successfully.")
        print(f"ID: {user.id}")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Created: {user.created_at}")

    except Exception as error:
        # If something goes wrong, undo the transaction.
        db.rollback()

        print("Failed to create test user.")
        print(f"Error: {error}")

    finally:
        # Always close the database connection.
        db.close()


# Run the function when this file is executed directly.
if __name__ == "__main__":
    create_test_user()
