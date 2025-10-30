"""Add saved recipes

Revision ID: af15d10833dd
Revises: ab61beb83573
Create Date: 2025-10-30 06:35:29.817586

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "af15d10833dd"
down_revision: Union[str, Sequence[str], None] = "ab61beb83573"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "saved_recipes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.id"],
            name=op.f("fk_saved_recipes_recipe_id_recipes"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_saved_recipes_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_saved_recipes")),
        sa.UniqueConstraint("user_id", "recipe_id", name="uq_user_recipe"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("saved_recipes")
