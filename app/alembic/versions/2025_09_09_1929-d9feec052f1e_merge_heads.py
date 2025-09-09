"""merge heads

Revision ID: d9feec052f1e
Revises: e15e791a760e, 32289814be39
Create Date: 2025-09-09 19:29:02.847669

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d9feec052f1e"
down_revision: Union[str, Sequence[str], None] = (
    "e15e791a760e",
    "32289814be39",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
