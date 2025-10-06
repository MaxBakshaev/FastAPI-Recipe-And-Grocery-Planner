"""Calories_per_unit now optional

Revision ID: a1c9d104bf6f
Revises: 10aff5bf2197
Create Date: 2025-10-06 08:16:44.371600

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1c9d104bf6f"
down_revision: Union[str, Sequence[str], None] = "10aff5bf2197"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "recipe_product_association",
        "calories_per_unit",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
        existing_server_default=sa.text("0"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "recipe_product_association",
        "calories_per_unit",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        existing_server_default=sa.text("0"),
    )
