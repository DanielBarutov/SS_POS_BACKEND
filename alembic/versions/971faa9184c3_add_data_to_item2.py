"""add data to Item2

Revision ID: 971faa9184c3
Revises: e635e7e6f3fe
Create Date: 2026-02-21 09:07:15.696463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '971faa9184c3'
down_revision: Union[str, Sequence[str], None] = 'e635e7e6f3fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
