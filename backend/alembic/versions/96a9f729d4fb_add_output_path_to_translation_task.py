"""add output_path to translation task

Revision ID: 96a9f729d4fb
Revises: a1b2c3d4e5f6
Create Date: 2026-02-12 12:11:46.722176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96a9f729d4fb'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('translation_tasks', sa.Column('output_path', sa.Text(), nullable=True))

def downgrade() -> None:
    op.drop_column('translation_tasks', 'output_path')
