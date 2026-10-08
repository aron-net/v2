# ---------------------------------------------------------
# Role Database Model
# ---------------------------------------------------------
#
# A role represents a group of permissions assigned to users.
#
# Examples:
#   ADMIN
#   FINANCE
#   HR
#   PROCUREMENT
#   AUDITOR
#   USER
#
# Roles will later be connected to:
#
#   User
#      ↓
#   UserRole
#      ↓
#   Role
#      ↓
#   RolePermission
#      ↓
#   Permission
#
# This allows administrators to create custom roles without
# changing the database structure.
# ---------------------------------------------------------

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Role(Base):
    """
    Database model representing a user role.
    """

    __tablename__ = "roles"

    # -----------------------------------------------------
    # Primary Key
    # -----------------------------------------------------
    #
    # UUID gives every role a globally unique identifier.
    # -----------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -----------------------------------------------------
    # Role Name
    # -----------------------------------------------------
    #
    # Examples:
    #   ADMIN
    #   FINANCE
    #   PROCUREMENT
    # -----------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    # -----------------------------------------------------
    # Description
    # -----------------------------------------------------

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # -----------------------------------------------------
    # System Role
    # -----------------------------------------------------
    #
    # True  = protected/system role
    # False = custom role created by an administrator
    #
    # We will use this later to prevent accidental deletion
    # of important system roles such as ADMIN.
    # -----------------------------------------------------

    is_system: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    # -----------------------------------------------------
    # Created At
    # -----------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
