"""add paymenttypedel

Revision ID: 4d2b0b9b1b53
Revises: 7619dbb61400
Create Date: 2026-02-21 19:54:38.942930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4d2b0b9b1b53'
down_revision: Union[str, Sequence[str], None] = '7619dbb61400'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    
    pass
