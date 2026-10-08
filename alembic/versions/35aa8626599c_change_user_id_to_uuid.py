"""
change user id to uuid

Revision ID: 35aa8626599c
Revises: a775dc48f3ca
Create Date: 2026-10-08 08:59:44.296788
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ---------------------------------------------------------
# Revision identifiers, used by Alembic.
# ---------------------------------------------------------

revision: str = "35aa8626599c"

down_revision: Union[str, Sequence[str], None] = "a775dc48f3ca"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


# ---------------------------------------------------------
# Upgrade
# ---------------------------------------------------------

def upgrade() -> None:
    """
    Change users.id from INTEGER to UUID.

    The users table is currently empty, so we can safely
    replace the primary-key column.

    PostgreSQL's pgcrypto extension provides gen_random_uuid()
    for automatic UUID generation.
    """

    # Enable PostgreSQL UUID generation.
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    # Remove the existing integer primary-key constraint.
    op.drop_constraint(
        "users_pkey",
        "users",
        type_="primary",
    )

    # Remove the old integer ID column.
    op.drop_column(
        "users",
        "id",
    )

    # Add the new UUID ID column.
    op.add_column(
        "users",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
    )

    # Make the UUID the primary key.
    op.create_primary_key(
        "users_pkey",
        "users",
        ["id"],
    )

    # Password hashes are required for every new user.
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=False,
    )


# ---------------------------------------------------------
# Downgrade
# ---------------------------------------------------------

def downgrade() -> None:
    """
    Revert the users ID back to INTEGER.

    This downgrade is intended for development because
    UUID values cannot be automatically converted back to
    the original integer IDs.
    """

    # Remove the UUID primary key.
    op.drop_constraint(
        "users_pkey",
        "users",
        type_="primary",
    )

    # Remove the UUID ID column.
    op.drop_column(
        "users",
        "id",
    )

    # Restore the integer ID column.
    op.add_column(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
    )

    # Restore the primary key.
    op.create_primary_key(
        "users_pkey",
        "users",
        ["id"],
    )

    # Allow password_hash to be nullable again.
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=True,
    )