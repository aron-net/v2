# ============================================================
# BPU NEXUS - PASSWORD RESET TOKEN MODEL
# ============================================================

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PasswordResetToken(Base):
    """
    Stores temporary password-reset codes.

    Reset codes:
        - belong to a user
        - expire after a short period
        - can only be used once
        - are stored as hashes instead of plain text
    """

    __tablename__ = "password_reset_tokens"

    # --------------------------------------------------------
    # ID
    # --------------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # --------------------------------------------------------
    # USER ID
    # --------------------------------------------------------
    #
    # Connects the reset request to the user account.
    #
    # --------------------------------------------------------

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # --------------------------------------------------------
    # CODE HASH
    # --------------------------------------------------------
    #
    # We do NOT store the actual reset code.
    # Only its hash is stored in the database.
    #
    # --------------------------------------------------------

    code_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # --------------------------------------------------------
    # EXPIRATION TIME
    # --------------------------------------------------------

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    # --------------------------------------------------------
    # USED TIME
    # --------------------------------------------------------
    #
    # NULL = code has not been used.
    # A timestamp = code has already been used.
    #
    # --------------------------------------------------------

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # --------------------------------------------------------
    # CREATED TIME
    # --------------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )