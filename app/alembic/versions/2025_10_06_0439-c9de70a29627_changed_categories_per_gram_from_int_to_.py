"""Changed categories_per_gram from int to float

Revision ID: c9de70a29627
Revises: 42854d3b8a9c
Create Date: 2025-10-06 04:39:04.741770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c9de70a29627'
down_revision: Union[str, Sequence[str], None] = '42854d3b8a9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('products', 'calories_per_gram',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False,
               existing_server_default=sa.text('0'))


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('products', 'calories_per_gram',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               existing_server_default=sa.text('0'))
