"""add payment

Revision ID: 1536b39a3017
Revises: 4d2b0b9b1b53
Create Date: 2026-02-21 20:06:03.739612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1536b39a3017'
down_revision: Union[str, Sequence[str], None] = '4d2b0b9b1b53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Сначала создаем сам тип ENUM в PostgreSQL
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

