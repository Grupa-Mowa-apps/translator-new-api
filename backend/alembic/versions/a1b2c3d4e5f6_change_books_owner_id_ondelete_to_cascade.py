"""change books owner_id ondelete to CASCADE

Revision ID: a1b2c3d4e5f6
Revises: 712a71d3547d
Create Date: 2025-01-20 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '712a71d3547d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing foreign key constraint
    op.drop_constraint('books_owner_id_fkey', 'books', type_='foreignkey')
    
    # Add new foreign key constraint with CASCADE
    op.create_foreign_key(
        'books_owner_id_fkey',
        'books',
        'users',
        ['owner_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop CASCADE foreign key constraint
    op.drop_constraint('books_owner_id_fkey', 'books', type_='foreignkey')
    
    # Restore RESTRICT foreign key constraint
    op.create_foreign_key(
        'books_owner_id_fkey',
        'books',
        'users',
        ['owner_id'],
        ['id'],
        ondelete='RESTRICT'
    )
