"""remove unused permissions and procurement tables

Revision ID: 9bb11eee011d
Revises: fd37d56a1b0a
Create Date: 2026-10-08 21:25:02.585461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bb11eee011d'
down_revision: Union[str, Sequence[str], None] = 'fd37d56a1b0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove database tables that are no longer used."""

    # Drop tables that depend on roles/users first.
    op.drop_table("role_permissions")
    op.drop_table("user_roles")

    # Remove the old permissions table.
    op.drop_table("permissions")

    # Remove the old procurement table.
    op.drop_table("procurements")


def downgrade() -> None:
    """This cleanup migration is intentionally not reversible."""

    raise NotImplementedError(
        "Downgrade is not supported for this cleanup migration."
    )