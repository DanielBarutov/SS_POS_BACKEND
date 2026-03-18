"""add data to Item

Revision ID: e635e7e6f3fe
Revises: e8527368d93b
Create Date: 2026-02-21 08:55:25.680321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e635e7e6f3fe'
down_revision: Union[str, Sequence[str], None] = 'e8527368d93b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
