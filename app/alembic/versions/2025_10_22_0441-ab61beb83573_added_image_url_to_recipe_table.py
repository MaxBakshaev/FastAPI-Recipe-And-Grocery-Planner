"""Added image_url to Recipe table

Revision ID: ab61beb83573
Revises: 7b2ebabce60c
Create Date: 2025-10-22 04:41:04.115421

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ab61beb83573"
down_revision: Union[str, Sequence[str], None] = "7b2ebabce60c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "recipes",
        sa.Column(
            "image_url",
            sa.String(length=500),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("recipes", "image_url")
