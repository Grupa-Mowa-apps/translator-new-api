"""Add chapter_number and title to chapter

Revision ID: 94d90b19dc87
Revises: 68a2e4e2bb4c
Create Date: 2025-10-15 12:35:14.303623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94d90b19dc87'
down_revision: Union[str, Sequence[str], None] = '68a2e4e2bb4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("chapters", sa.Column("chapter_number", sa.Integer(), nullable=False))
    op.add_column("chapters", sa.Column("title", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("chapters", "chapter_number")
    op.drop_column("chapters", "title")
