"""fix address in order model

Revision ID: 801a197d00bc
Revises: 1536b39a3017
Create Date: 2026-02-26 18:23:35.781908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '801a197d00bc'
down_revision: Union[str, Sequence[str], None] = '1536b39a3017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('orders', 'address_id')
    op.add_column('orders', sa.Column(
        'address_id', sa.Integer(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('orders', sa.Column(
        'address_id', sa.Integer(), nullable=True))
