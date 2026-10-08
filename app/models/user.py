import uuid

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    """
    User database model.

    This class represents the 'users' table in PostgreSQL.
    Each instance of User represents one row in that table.
    """

    # Tell SQLAlchemy that this model should create/use
    # a PostgreSQL table called 'users'.
    __tablename__ = "users"

    # Automatically generated UUID for every user.
    #
    # UUIDs are globally unique and are safer to expose through
    # APIs than sequential numeric IDs.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # User's full name.
    # Maximum length is 100 characters.
    # nullable=False means the name is required.
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # User's email address.
    # Maximum length is 255 characters.
    # nullable=False means every user must have an email.
    # unique=True prevents two users from using the same email.
    # index=True creates a database index to make email searches faster.
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    # Password hash generated from the user's password.
    #
    # We NEVER store plain text passwords.
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # User's role in the system.
    # For now, a new user defaults to the USER role.
    #
    # Later we can have roles such as:
    # ADMIN, APPROVER, PROCUREMENT, etc.
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="USER",
    )

    # Date and time when the user was created.
    # SQLAlchemy will automatically set this value when
    # a new User object is created.
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )