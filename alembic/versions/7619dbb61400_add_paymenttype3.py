"""add paymenttype3

Revision ID: 7619dbb61400
Revises: b883e0f3379c
Create Date: 2026-02-21 19:46:23.818219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7619dbb61400'
down_revision: Union[str, Sequence[str], None] = 'b883e0f3379c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
