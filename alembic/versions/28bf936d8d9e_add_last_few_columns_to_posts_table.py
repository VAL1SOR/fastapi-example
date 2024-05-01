"""add last few columns to posts table

Revision ID: 28bf936d8d9e
Revises: f86762589431
Create Date: 2024-05-01 04:42:16.071790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28bf936d8d9e'
down_revision: Union[str, None] = 'f86762589431'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('time', sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text('NOW()')),)


def downgrade() -> None:
    op.drop_column('posts', 'time')
