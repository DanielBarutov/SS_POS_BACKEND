"""add paymenttype2

Revision ID: b883e0f3379c
Revises: f997cc1488d5
Create Date: 2026-02-21 11:51:26.160585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b883e0f3379c'
down_revision: Union[str, Sequence[str], None] = 'f997cc1488d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Сначала создаем сам тип ENUM в PostgreSQL
    payment_type_enum = postgresql.ENUM('cash', 'card', name='paymenttype')
    payment_type_enum.create(op.get_bind())

    # 2. Добавляем колонку в таблицу orders
    op.add_column('orders', sa.Column('payment_type', sa.Enum('cash', 'card', name='paymenttype'), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Удаляем колонку
    op.drop_column('orders', 'payment_type')
    
    # 2. Удаляем тип из базы
    op.execute("DROP TYPE paymenttype")
