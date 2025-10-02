"""created association table, updated recipe and product tables

Revision ID: e5a2f8f2f928
Revises: b68d46f90064
Create Date: 2025-10-02 04:56:08.281918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e5a2f8f2f928'
down_revision: Union[str, Sequence[str], None] = 'b68d46f90064'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('recipe_product_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), server_default='0', nullable=False),
    sa.Column('calories_per_unit', sa.Integer(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name=op.f('fk_recipe_product_association_product_id_products')),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], name=op.f('fk_recipe_product_association_recipe_id_recipes')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_recipe_product_association')),
    sa.UniqueConstraint('recipe_id', 'product_id', name='uq_recipe_product')
    )
    op.add_column('products', sa.Column('calories_per_gram', sa.Integer(), server_default='0', nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'calories_per_gram')
    op.drop_table('recipe_product_association')
