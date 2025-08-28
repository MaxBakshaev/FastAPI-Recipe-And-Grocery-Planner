"""Add email and hashed_password to user

Revision ID: ffcd9701cf5b
Revises: 2d1731c5bfe1
Create Date: 2025-08-28 12:05:57.680631

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ffcd9701cf5b"
down_revision: Union[str, Sequence[str], None] = "2d1731c5bfe1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("email", sa.String(), nullable=False))
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(), nullable=False)
    )
    op.create_unique_constraint(op.f("uq_users_email"), "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("uq_users_email"), "users", type_="unique")
    op.drop_column("users", "hashed_password")
    op.drop_column("users", "email")
