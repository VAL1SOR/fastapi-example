"""add content column to posts table

Revision ID: fcd62ddc5c30
Revises: e8b1b8b438b6
Create Date: 2024-05-01 04:16:08.679038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcd62ddc5c30'
down_revision: Union[str, None] = 'e8b1b8b438b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
