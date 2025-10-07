"""Renamed calories_per_unit to calories_per_gram

Revision ID: 7b2ebabce60c
Revises: a1c9d104bf6f
Create Date: 2025-10-07 06:45:08.557938

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7b2ebabce60c"
down_revision: Union[str, Sequence[str], None] = "a1c9d104bf6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "recipe_product_association",
        sa.Column(
            "calories_per_gram",
            sa.Float(),
            server_default="0",
            nullable=False,
        ),
    )
    op.drop_column("recipe_product_association", "calories_per_unit")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "recipe_product_association",
        sa.Column(
            "calories_per_unit",
            sa.DOUBLE_PRECISION(precision=53),
            server_default=sa.text("0"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("recipe_product_association", "calories_per_gram")
