"""add paymenttype

Revision ID: f997cc1488d5
Revises: 967e3d03dc91
Create Date: 2026-02-21 11:46:39.425698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f997cc1488d5'
down_revision: Union[str, Sequence[str], None] = '967e3d03dc91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
