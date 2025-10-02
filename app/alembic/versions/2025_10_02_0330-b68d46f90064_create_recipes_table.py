"""create recipes table

Revision ID: b68d46f90064
Revises: 3f00c6ea3673
Create Date: 2025-10-02 03:30:48.091540

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b68d46f90064"
down_revision: Union[str, Sequence[str], None] = "3f00c6ea3673"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "recipes",
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("body", sa.Text(), server_default="", nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_recipes_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_recipes")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("recipes")
