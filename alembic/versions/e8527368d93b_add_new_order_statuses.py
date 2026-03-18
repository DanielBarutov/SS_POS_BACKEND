"""add_new_order_statuses

Revision ID: e8527368d93b
Revises: f01979cafb72
Create Date: 2026-02-20 21:17:11.275680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8527368d93b'
down_revision: Union[str, Sequence[str], None] = 'f01979cafb72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("COMMIT") 
    op.execute("ALTER TYPE orderstatus ADD VALUE 'completed_not_paid'")
    op.execute("ALTER TYPE orderstatus ADD VALUE 'completed_paid'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
