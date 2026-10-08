"""
add password hash to users

Revision ID: a775dc48f3ca
Revises: 63acf02f52eb
Create Date: 2026-10-08 00:48:47.063262
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ---------------------------------------------------------
# Revision identifiers, used by Alembic.
# ---------------------------------------------------------

revision: str = "a775dc48f3ca"

down_revision: Union[str, Sequence[str], None] = "63acf02f52eb"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


# ---------------------------------------------------------
# Upgrade
# ---------------------------------------------------------

def upgrade() -> None:
    """
    Add the password_hash column to the users table.

    The column is temporarily nullable because the database
    already contains existing users.

    We will populate password hashes before making the
    column required.
    """

    op.add_column(
        "users",
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=True,
        ),
    )


# ---------------------------------------------------------
# Downgrade
# ---------------------------------------------------------

def downgrade() -> None:
    """
    Remove the password_hash column.
    """

    op.drop_column(
        "users",
        "password_hash",
    )