"""add_created_at_to_items

Revision ID: 967e3d03dc91
Revises: eb5061def573
Create Date: 2026-02-21 09:11:28.492175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '967e3d03dc91'
down_revision: Union[str, Sequence[str], None] = 'eb5061def573'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('order_items', sa.Column('created_at', sa.DateTime(timezone=True), 
               server_default=sa.text('now()'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('order_items', 'created_at')
