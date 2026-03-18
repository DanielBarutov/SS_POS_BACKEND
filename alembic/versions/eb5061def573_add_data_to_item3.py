"""add data to Item3

Revision ID: eb5061def573
Revises: 971faa9184c3
Create Date: 2026-02-21 09:09:44.572136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb5061def573'
down_revision: Union[str, Sequence[str], None] = '971faa9184c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
